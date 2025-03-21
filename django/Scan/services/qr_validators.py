# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022 Brennen Chiu

import shutil

from django.conf import settings
from Papers.services import SpecificationService
from Scan.models import StagingImage
from Papers.models import ErrorImage
from collections import Counter
from Papers.services import ImageBundleService


class QRErrorService:
    def check_qr_codes(self, page_data, image_path):
        """
        Check integrity of QR codes on a page.
        """
        spec_service = SpecificationService()
        spec_dictionary = spec_service.get_the_spec()
        img_obj = StagingImage.objects.get(file_path=image_path)

        serialized_top_three_qr = self.serialize_qr_code(page_data, "top_3")
        serialized_all_qr = self.serialize_qr_code(page_data, "all")
        serialized_public_code = self.serialize_qr_code(page_data, "public_code")

        self.check_TPV_code(serialized_all_qr, img_obj, serialized_top_three_qr)
        self.check_qr_numbers(page_data, img_obj, serialized_top_three_qr)
        self.check_qr_matching(
            serialized_top_three_qr, img_obj, serialized_top_three_qr
        )
        self.check_public_code(
            serialized_public_code, spec_dictionary, img_obj, serialized_top_three_qr
        )

    def serialize_qr_code(self, page_data, tpv_type):
        """
        Function to serialize QR code based on tpv type.
        tpv_type:
                  top_3:    get the top 3 tpv codes.
                    all:    get all the tpv codes.
            public_code:    get tpv public codes.
        """
        qr_code_list = []
        for q in page_data:
            paper_id = list(page_data[q].values())[0]
            page_num = list(page_data[q].values())[1]
            version_num = list(page_data[q].values())[2]
            quadrant = list(page_data[q].values())[3]
            public_code = list(page_data[q].values())[4]

            if tpv_type == "top_3":
                qr_code_list.append(paper_id + page_num + version_num)
            elif tpv_type == "all":
                qr_code_list.append(
                    paper_id + page_num + version_num + quadrant + public_code
                )
            elif tpv_type == "public_code":
                qr_code_list.append(public_code)
            else:
                raise ValueError("No specific TPV type.")
        return qr_code_list

    def check_TPV_code(self, qr_list, img_obj, top_three_tpv):
        """
        Check if TPV codes are 17 digits long.
        """
        for indx in qr_list:
            if len(indx) != len("TTTTTPPPVVVOCCCCC"):
                self.create_error_image(img_obj, top_three_tpv)
                img_obj.error = True
                img_obj.save()
                raise ValueError("Invalid QR code.")

    def check_qr_numbers(self, page_data, img_obj, top_three_tpv):
        """
        Check number of QR codes in a given page.
        """
        if len(page_data) == 0:
            img_obj.unknown = True
            img_obj.save()
            raise ValueError("Unable to read QR codes.")
        elif len(page_data) <= 2:
            # self.create_error_image(img_obj)
            self.create_error_image(img_obj, top_three_tpv)
            img_obj.error = True
            img_obj.save()
            raise ValueError("Detect less than 3 QR codes.")
        elif len(page_data) == 3:
            pass
        else:
            self.create_error_image(img_obj, top_three_tpv)
            img_obj.error = True
            img_obj.save()
            raise ValueError("Detected more than 3 QR codes.")

    def check_qr_matching(self, qr_list, img_obj, top_three_tpv):
        """
        Check if QR codes matches.
        This is to check if a page is folded.
        """
        for indx in range(1, len(qr_list)):
            if qr_list[indx] == qr_list[indx - 1]:
                pass
            else:
                self.create_error_image(img_obj, top_three_tpv)
                img_obj.error = True
                img_obj.save()
                raise ValueError("QR codes do not match.")

    def check_public_code(self, public_codes, spec_dictionary, img_obj, top_three_tpv):
        """
        Check if the paper public QR code matches with spec public code.
        """
        spec_public_code = spec_dictionary["publicCode"]
        for public_code in public_codes:
            if public_code == str(spec_public_code):
                pass
            else:
                self.create_error_image(img_obj, top_three_tpv)
                img_obj.error = True
                img_obj.save()
                raise ValueError(
                    f"Magic code {public_code} did not match spec {spec_public_code}. Did you scan the wrong test?"
                )

    def create_error_image(self, img_obj, top_three_tpv):
        if not ErrorImage.objects.filter(hash=img_obj.image_hash).exists():

            img_bundle_service = ImageBundleService()
            counter = Counter(top_three_tpv)
            most_common_qr = counter.most_common(1)
            common_qr = most_common_qr[0][0]

            test_paper = common_qr[0:5]
            page_number = common_qr[5:8]
            version_number = common_qr[8:]

            root_folder = settings.BASE_DIR / "media" / "page_images" / "error_pages"
            test_folder = root_folder / str(test_paper)
            img_path = test_folder / f"page{page_number}_{img_obj.image_hash}.png"

            staged_bundle = img_obj.bundle
            bundle = img_bundle_service.get_or_create_bundle(
                staged_bundle.slug, staged_bundle.pdf_hash
            )

            error_image = ErrorImage(
                bundle=bundle,
                bundle_order=img_obj.bundle_order,
                original_name=img_obj.file_name,
                file_name=str(img_path),
                hash=img_obj.image_hash,
                rotation=img_obj.rotation,
                paper_number=int(test_paper),
                page_number=int(page_number),
                version_number=int(version_number),
            )
            error_image.save()

            root_folder.mkdir(exist_ok=True)
            test_folder.mkdir(exist_ok=True)
            shutil.copy(img_obj.file_path, img_path)

    def create_unknown_image(self, img_obj):
        pass
