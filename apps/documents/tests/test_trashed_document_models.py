from ..models import Document, TrashedDocument

from .base import GenericDocumentTestCase


class TrashedDocumentTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_restoring_documents(self):
        self.assertEqual(Document.valid.count(), 1)

        # Trash the document
        self._test_document.delete()
        self.assertEqual(TrashedDocument.objects.count(), 1)
        self.assertEqual(Document.valid.count(), 0)

        # Restore the document
        TrashedDocument.objects.get(
            pk=self._test_document.pk
        ).restore(user=self._test_case_user)
        self.assertEqual(TrashedDocument.objects.count(), 0)
        self.assertEqual(Document.valid.count(), 1)

    def test_trashing_documents(self):
        self.assertEqual(Document.valid.count(), 1)

        # Trash the document
        self._test_document.delete()
        self.assertEqual(TrashedDocument.objects.count(), 1)
        self.assertEqual(Document.valid.count(), 0)

        # Delete the document
        self._test_document.delete()
        self.assertEqual(TrashedDocument.objects.count(), 0)
        self.assertEqual(Document.valid.count(), 0)


class TrashedDocumentPageTestCase(GenericDocumentTestCase):
    def test_trashed_document_page_count(self):
        page_count = self._test_document.version_active.pages.count()
        self._test_document.delete()
        test_trashed_document = TrashedDocument.objects.get(
            pk=self._test_document.pk
        )
        self.assertTrue(
            test_trashed_document.version_active.pages.count(), page_count
        )


class TrashedDocumentAPITestCase(GenericDocumentTestCase):
    def test_trashed_document_api_image_re_path(self):
        self._test_document.delete()
        test_trashed_document = TrashedDocument.objects.get(
            pk=self._test_document.pk
        )

        self._clear_events()

        self.assertTrue(
            test_trashed_document.get_api_image_re_path()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
