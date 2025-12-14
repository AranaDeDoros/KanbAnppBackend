from rest_framework.throttling import UserRateThrottle

class AttachmentUploadThrottle(UserRateThrottle):
    scope = "attachment_upload"

