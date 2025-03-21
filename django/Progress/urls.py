# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022 Edith Coates
# Copyright (C) 2022 Brennen Chiu

from django.urls import path

from Progress.views import (
    ScanOverview,
    ScanTestPaperProgress,
    ScanGetPageImage,
    ScanTestPageModal,
    ScanBundles,
    ScanColliding,
    CollidingPagesModal,
    CollisionPageImage,
    DiscardCollidingPage,
    ReplaceImageWithColliding,
    ScanUnknown,
    ScanError,
    ErrorPagesModal,
    ErrorPageImage,
    ScanExtra,
    ScanDiscarded,
    DiscardedPageImage,
    DiscardedPageModal,
    DeleteDiscardedPage,
    RestoreDiscardedPage,
)


urlpatterns = [
    path("scan/overview/", ScanOverview.as_view(), name="progress_scan_overview"),
    path(
        "scan/overview/<filter_by>",
        ScanTestPaperProgress.as_view(),
        name="progress_scan_tptable",
    ),
    path(
        "scan/overview/<int:test_paper>/<int:index>/img/",
        ScanGetPageImage.as_view(),
        name="progress_scan_page_image",
    ),
    path(
        "scan/overview/<int:test_paper>/<int:index>/",
        ScanTestPageModal.as_view(),
        name="progress_scan_page_modal",
    ),
    path("scan/bundles/", ScanBundles.as_view(), name="progress_scan_bundles"),
    path("scan/colliding/", ScanColliding.as_view(), name="progress_scan_colliding"),
    path(
        "scan/colliding/<int:test_paper>/<int:index>/<colliding_hash>",
        CollidingPagesModal.as_view(),
        name="progress_colliding_modal",
    ),
    path(
        "scan/colliding/get/<colliding_hash>/",
        CollisionPageImage.as_view(),
        name="progress_collision_image",
    ),
    path(
        "scan/colliding/delete/<colliding_hash>/",
        DiscardCollidingPage.as_view(),
        name="progress_discard_colliding",
    ),
    path(
        "scan/colliding/delete/<int:test_paper>/<int:index>/<colliding_hash>/",
        ReplaceImageWithColliding.as_view(),
        name="progress_replace_colliding",
    ),
    path("scan/unknown/", ScanUnknown.as_view(), name="progress_scan_unknown"),
    path("scan/error/", ScanError.as_view(), name="progress_scan_error"),
    path(
        "scan/error/<int:test_paper>/<int:page_number>/<hash>/",
        ErrorPagesModal.as_view(),
        name="progress_error_modal",
    ),
    path(
        "scan/error/get/<hash>",
        ErrorPageImage.as_view(),
        name="progress_error_image",
    ),
    path("scan/extra/", ScanExtra.as_view(), name="progress_scan_extra"),
    path("scan/discarded/", ScanDiscarded.as_view(), name="progress_scan_discarded"),
    path(
        "scan/discarded/get/<discarded_hash>/",
        DiscardedPageImage.as_view(),
        name="progress_scan_discarded_image",
    ),
    path(
        "scan/discarded/view/<discarded_hash>/",
        DiscardedPageModal.as_view(),
        name="progress_discarded_modal",
    ),
    path(
        "scan/discarded/delete/<discarded_hash>/",
        DeleteDiscardedPage.as_view(),
        name="progress_delete_discarded",
    ),
    path(
        "scan/discarded/restore/<discarded_hash>/",
        RestoreDiscardedPage.as_view(),
        name="progress_restore_discarded",
    ),
]
