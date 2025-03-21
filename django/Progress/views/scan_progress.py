# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022 Edith Coates

from django.shortcuts import render

from Base.base_group_views import ManagerRequiredView

from Progress.services import ManageScanService
from Progress.views import BaseScanProgressPage


class ScanBundles(BaseScanProgressPage):
    """
    View the bundles uploaded by scanner users.
    """

    def get(self, request):
        context = self.build_context("bundles")
        mss = ManageScanService()

        context.update(
            {
                "n_bundles": mss.get_n_bundles(),
                "bundles": mss.get_bundles_list(),
            }
        )
        return render(request, "Progress/scan_bundles.html", context)


class ScanUnknown(BaseScanProgressPage):
    """
    View and manage unknown pages.
    """

    def get(self, request):
        context = self.build_context("unknown_page")
        return render(request, "Progress/scan_unknown.html", context)


class ScanExtra(BaseScanProgressPage):
    """
    View and manage extra pages.
    """

    def get(self, request):
        context = self.build_context("extra")
        return render(request, "Progress/scan_extra.html", context)
