# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022 Edith Coates
# Copyright (C) 2022 Brennen Chiu

import pathlib

from django.shortcuts import render
from django.template.loader import render_to_string

from django.http import FileResponse
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile

from Preparation.services import PQVMappingService, StagingStudentService
from SpecCreator.services import StagingSpecificationService
from Papers.services import SpecificationService, PaperInfoService

from .services import BuildPapersService, RenamePDFFile
from .models import PDFTask
from Base.base_group_views import ManagerRequiredView


class BuildPaperPDFs(ManagerRequiredView):
    template_name = "BuildPaperPDF/build_paper_pdfs.html"

    def table_fragment(self, request):
        """Get the current state of the tasks, render it as an HTML table, and return"""
        bps = BuildPapersService()
        rename = RenamePDFFile()

        tasks = PDFTask.objects.all()
        names = [rename.get_PDF_name(t.pdf_file_path) for t in tasks]
        task_context = zip(tasks, names)

        running_tasks = bps.get_n_running_tasks()
        if running_tasks > 0:
            poll = True
        else:
            poll = False

        table_fragment = render_to_string(
            "BuildPaperPDF/fragments/pdf_table.html",
            {"tasks": task_context, "poll": poll},
            request=request,
        )

        return table_fragment

    def get(self, request):
        bps = BuildPapersService()
        pqvs = PQVMappingService()
        pinfo = PaperInfoService()
        qvmap = pqvs.get_pqv_map_dict()
        num_pdfs = len(qvmap)

        n_tasks = bps.get_n_tasks()
        if n_tasks > 0:
            pdfs_staged = True
        else:
            pdfs_staged = False

        table_fragment = self.table_fragment(request)

        zip_disabled = True
        n_completed_tasks = bps.get_n_complete_tasks()
        if n_completed_tasks == n_tasks:
            zip_disabled = False

        context = self.build_context()
        context.update(
            {
                "message": "",
                "zip_disabled": zip_disabled,
                "num_pdfs": num_pdfs,
                "pdfs_staged": pdfs_staged,
                "pdf_table": table_fragment,
                "db_initialised": pinfo.is_paper_database_populated(),
            }
        )

        return render(request, self.template_name, context)

    def post(self, request):
        bps = BuildPapersService()
        pqvs = PQVMappingService()
        qvmap = pqvs.get_pqv_map_dict()
        num_pdfs = len(qvmap)
        sstu = StagingStudentService()
        classdict = sstu.get_classdict()

        bps.clear_tasks()
        # print(classdict)
        bps.stage_pdf_jobs(num_pdfs, classdict=classdict)

        task_objects = PDFTask.objects.all()
        Rename = RenamePDFFile()

        tasks_paper_number = []
        tasks_pdf_file_path = []
        tasks_status = []

        for task in task_objects:
            tasks_paper_number.append(task.paper_number)
            tasks_pdf_file_path.append(Rename.get_PDF_name(task.pdf_file_path))
            tasks_status.append(task.status)

        table_fragment = self.table_fragment(request)

        context = self.build_context()
        context.update(
            {
                "message": "",
                "tasks": zip(task_objects, tasks_pdf_file_path),
                "zip_disabled": True,
                "pdfs_staged": True,
                "pdf_table": table_fragment,
            }
        )

        return render(request, self.template_name, context)


class PDFTableView(ManagerRequiredView):
    def render_pdf_table(self, request):
        task_objects = PDFTask.objects.all()
        bps = BuildPapersService()
        Rename = RenamePDFFile()
        tasks_pdf_file_path = []

        for task in task_objects:
            tasks_pdf_file_path.append(Rename.get_PDF_name(task.pdf_file_path))

        n_complete = bps.get_n_complete_tasks()
        n_total = len(task_objects)
        if n_total > 0:
            percent_complete = n_complete / n_total * 100
        else:
            percent_complete = 0

        zip_disabled = True
        status = 200
        if n_complete == n_total:
            status = 286
            zip_disabled = False

        n_running = bps.get_n_running_tasks()
        poll = n_running > 0

        context = self.build_context()
        context.update(
            {
                "tasks": zip(task_objects, tasks_pdf_file_path),
                "pdf_errors": bps.are_there_errors(),
                "message": f"Progress: {n_complete} papers of {n_total} built ({percent_complete:.0f}%)",
                "zip_disabled": zip_disabled,
                "poll": poll,
            }
        )

        return render(
            request, "BuildPaperPDF/fragments/pdf_table.html", context, status=status
        )


class UpdatePDFTable(PDFTableView):
    """Get an updated pdf-building-progress table"""

    def get(self, request):
        return self.render_pdf_table(request)


class GetPDFFile(ManagerRequiredView):
    def get(self, request, paper_number):
        pdf_file = PDFTask.objects.get(paper_number=paper_number).pdf_file_path
        pdf_path = pathlib.Path(pdf_file)
        if not pdf_path.exists() or not pdf_path.is_file():
            return HttpResponse(status=500)

        pdf_file_name = RenamePDFFile().get_PDF_name(pdf_file)
        file = pdf_path.open("rb")
        pdf = SimpleUploadedFile(
            str(pdf_file_name), file.read(), content_type="application/pdf"
        )
        file.close()

        return FileResponse(pdf)


class GetCompressedPDFs(ManagerRequiredView):
    """Get the completed test paper PDFs in one zip file"""

    def post(self, request):
        bps = BuildPapersService()
        shortname = StagingSpecificationService().get_short_name_slug()
        save_path = bps.get_pdf_zipfile(filename=f"{shortname}.zip")
        zip_file = save_path.open("rb")
        zf = SimpleUploadedFile(
            save_path.name, zip_file.read(), content_type="application/zip"
        )
        zip_file.close()
        save_path.unlink()
        return FileResponse(zf)


class StartAllPDFs(PDFTableView):
    def post(self, request):
        bps = BuildPapersService()
        spec = SpecificationService().get_the_spec()
        pqvs = PQVMappingService()
        qvmap = pqvs.get_pqv_map_dict()

        bps.send_all_tasks(spec, qvmap)

        return self.render_pdf_table(request)


class StartOnePDF(PDFTableView):
    def post(self, request, paper_number):
        bps = BuildPapersService()
        spec = SpecificationService().get_the_spec()
        pqvs = PQVMappingService()
        qvmap = pqvs.get_pqv_map_dict()

        bps.send_single_task(paper_number, spec, qvmap[paper_number])

        return self.render_pdf_table(request)


class CancelAllPDf(PDFTableView):
    def post(self, request):
        bps = BuildPapersService()
        bps.cancel_all_task()

        return self.render_pdf_table(request)


class CancelOnePDF(PDFTableView):
    def post(self, request, paper_number):
        bps = BuildPapersService()
        bps.cancel_single_task(paper_number)

        return self.render_pdf_table(request)


class RetryAllPDF(PDFTableView):
    def post(self, request):
        bps = BuildPapersService()
        spec = SpecificationService().get_the_spec()
        pqvs = PQVMappingService()
        qvmap = pqvs.get_pqv_map_dict()

        bps.retry_all_task(spec, qvmap)

        return self.render_pdf_table(request)


class DeleteAllPDF(BuildPaperPDFs):
    template_name = "BuildPaperPDF/delete_paper_pdfs.html"

    def post(self, request):
        bps = BuildPapersService()
        bps.delete_all_task()
        pinfo = PaperInfoService()
        pqvs = PQVMappingService()
        qvmap = pqvs.get_pqv_map_dict()
        num_pdfs = len(qvmap)

        n_tasks = bps.get_n_tasks()
        if n_tasks > 0:
            pdfs_staged = True
        else:
            pdfs_staged = False

        table_fragment = self.table_fragment(request)

        zip_disabled = True
        n_completed_tasks = bps.get_n_complete_tasks()
        if n_completed_tasks == n_tasks:
            zip_disabled = False

        context = self.build_context()
        context.update(
            {
                "message": "",
                "zip_disabled": zip_disabled,
                "num_pdfs": num_pdfs,
                "pdfs_staged": pdfs_staged,
                "pdf_table": table_fragment,
                "db_initialised": pinfo.is_paper_database_populated(),
            }
        )

        return render(request, self.template_name, context)
