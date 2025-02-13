from datetime import timedelta

from ..events import event_document_type_changed
from ..models.document_models import Document
from ..models.document_type_models import DocumentType
from ..permissions import permission_document_change_type
from ..settings import setting_stub_expiration_interval

from .base import GenericDocumentTestCase
from .literals import (
    TEST_DOCUMENT_SMALL_CHECKSUM, TEST_FILE_SMALL_FILENAME,
    TEST_DOCUMENT_SMALL_MIMETYPE, TEST_DOCUMENT_SMALL_SIZE
)


class DocumentChangeTypeTestCase(GenericDocumentTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_document_type()

    def test_document_change_type_no_permission(self):
        test_document_type = self._test_document.document_type

        self._clear_events()

        with self.assertRaises(expected_exception=Document.DoesNotExist):
            self._test_document.document_type_change(
                document_type=self._test_document_type,
                user=self._test_case_user
            )

        self.assertEqual(
            self._test_document.document_type, test_document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_change_type_with_document_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_change_type
        )

        test_document_type = self._test_document.document_type

        self._clear_events()

        with self.assertRaises(expected_exception=DocumentType.DoesNotExist):
            self._test_document.document_type_change(
                document_type=self._test_document_type,
                user=self._test_case_user
            )

        self.assertEqual(
            self._test_document.document_type, test_document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_change_type_with_document_type_access(self):
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_change_type
        )

        test_document_type = self._test_document.document_type

        self._clear_events()

        with self.assertRaises(expected_exception=Document.DoesNotExist):
            self._test_document.document_type_change(
                document_type=self._test_document_type,
                user=self._test_case_user
            )

        self.assertEqual(
            self._test_document.document_type, test_document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_change_type_with_full_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_change_type
        )
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_change_type
        )

        test_document_type = self._test_document.document_type

        self._clear_events()

        self._test_document.document_type_change(
            document_type=self._test_document_type,
            user=self._test_case_user
        )

        self.assertNotEqual(
            self._test_document.document_type, test_document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_document_type_changed.id)

    def test_trashed_document_change_type_with_full_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_change_type
        )
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_change_type
        )

        test_document_type = self._test_document.document_type

        self._test_document.delete()

        self._clear_events()

        with self.assertRaises(expected_exception=Document.DoesNotExist):
            self._test_document.document_type_change(
                document_type=self._test_document_type,
                user=self._test_case_user
            )

        self.assertEqual(
            self._test_document.document_type, test_document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentTestCase(GenericDocumentTestCase):
    def test_document_creation(self):
        self.assertEqual(
            self._test_document.document_type.label,
            self._test_document_type.label
        )

        self.assertEqual(self._test_document.file_latest.exists(), True)
        self.assertEqual(
            self._test_document.file_latest.size,
            TEST_DOCUMENT_SMALL_SIZE
        )

        self.assertEqual(
            self._test_document.file_latest.mimetype,
            TEST_DOCUMENT_SMALL_MIMETYPE
        )
        self.assertEqual(
            self._test_document.file_latest.encoding, 'binary'
        )
        self.assertEqual(
            self._test_document.file_latest.checksum,
            TEST_DOCUMENT_SMALL_CHECKSUM
        )
        self.assertEqual(self._test_document.file_latest.pages.count(), 1)
        self.assertEqual(
            self._test_document.label, TEST_FILE_SMALL_FILENAME
        )

    def test_method_get_absolute_re_path(self):
        self._create_test_document_stub()

        self.assertTrue(self._test_document.get_absolute_re_path())


class DocumentManagerTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_document_stubs_deletion(self):
        document_stub = Document.objects.create(
            document_type=self._test_document_type
        )

        Document.objects.delete_stubs()

        self.assertEqual(Document.objects.count(), 1)

        document_stub.datetime_created = document_stub.datetime_created - timedelta(
            seconds=setting_stub_expiration_interval.value + 1
        )
        document_stub.save()

        Document.objects.delete_stubs()

        self.assertEqual(Document.objects.count(), 0)
