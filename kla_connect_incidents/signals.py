from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from kla_connect_incidents.models import KlaConnectReport, KlaConnectIncident, \
    INCIDENT_STATUS_COMPLETE, get_user_model
from kla_connect_utils.constants import FEEDBACK_CHANGE_VERB, REJECTED_VERB, \
    COMPLETED_VERB, CITIZEN_USER, INCIDENT_ALERT, REPORT_ALERT, INCIDENT_STATUS_FOR_REVIEW, \
    MANAGER_TRANSPORT, REPORT_REVIEW_VERB, INCIDENT_REPORT_REJECTED, UPDATED_VERB


@receiver(post_save, sender=KlaConnectIncident)
def handle_incident_update(sender, instance, created, **kwargs):
    if not created:
        feedbackchanged = (
            instance.previous_feedback is not None and instance.previous_feedback != instance.feedback)
        if feedbackchanged:
            notify.send(
                instance.author,
                recipient=instance.user,
                verb=FEEDBACK_CHANGE_VERB,
                action_object=instance,
                description="Added feedback to incident",
                public=False,
                author=instance.author.full_name,
                previous_feedback=instance.previous_feedback,
                current_feedback=instance.feedback
            )

        completed = (instance.previous_status is not None and instance.previous_status != instance.status
                     and instance.status == INCIDENT_STATUS_COMPLETE)
        if completed:
            notify.send(
                instance.author,
                recipient=instance.user,
                verb=COMPLETED_VERB,
                action_object=instance,
                level="success",
                description="Approved Incident",
                public=False,
                author=instance.author.full_name,
                previous_status=instance.previous_status,
                current_status=instance.status
            )
            # alert all citiziens except creator
            notify.send(
                instance.author,
                recipient=get_user_model().objects.filter(
                    role=CITIZEN_USER).exclude(id=instance.user.id),
                verb=INCIDENT_ALERT,
                action_object=instance,
                public=False,
                level="success",
                description="Reported Incident"
            )

        if not (completed or feedbackchanged):
            notify.send(
                instance.author,
                recipient=instance.user,
                verb=UPDATED_VERB,
                action_object=instance,
                level="success",
                description="Updated Incident",
                public=False,
                author=instance.author.full_name if instance.author else "System Activity",
                previous_status=instance.previous_status,
                current_status=instance.status
            )


@receiver(post_save, sender=KlaConnectReport)
def handle_report_update(sender, instance, created, **kwargs):
    if not created:
        feedbackchanged = (
            instance.previous_feedback is not None and instance.previous_feedback != instance.feedback)
        if feedbackchanged:
            notify.send(
                instance.author,
                recipient=instance.user,
                verb=FEEDBACK_CHANGE_VERB,
                action_object=instance,
                description="Added feedback to report",
                public=False,
                author=instance.author.full_name,
                previous_feedback=instance.previous_feedback,
                current_feedback=instance.feedback
            )

        forwarded_for_review = (instance.previous_status is not None and instance.previous_status != instance.status
                                and instance.status == INCIDENT_STATUS_FOR_REVIEW)
        if forwarded_for_review:
            notify.send(
                instance.author,
                recipient=get_user_model().objects.filter(
                    role=MANAGER_TRANSPORT).exclude(id=instance.user.id),
                verb=REPORT_REVIEW_VERB,
                action_object=instance,
                description="Report For Review",
                public=False,
                author=instance.author.full_name,
                previous_status=instance.previous_status,
                current_status=instance.status
            )

        rejected_report = (instance.previous_status is not None and instance.previous_status != instance.status
                           and instance.status == INCIDENT_REPORT_REJECTED)
        if rejected_report:
            notify.send(
                instance.author,
                recipient=instance.user,
                verb=REJECTED_VERB,
                action_object=instance,
                level="warning",
                description="Report Rejected",
                public=False,
                author=instance.author.full_name,
                previous_status=instance.previous_status,
                current_status=instance.status
            )

        completed = (instance.previous_status is not None and instance.previous_status != instance.status
                     and instance.status == INCIDENT_STATUS_COMPLETE)
        if completed:
            notify.send(
                instance.author,
                recipient=instance.user,
                verb=COMPLETED_VERB,
                action_object=instance,
                level="success",
                description="Approved Report",
                public=False,
                author=instance.author.full_name,
                previous_status=instance.previous_status,
                current_status=instance.status
            )

        if instance.publishing:
            # alert all citiziens
            notify.send(
                instance.author,
                recipient=get_user_model().objects.filter(role=CITIZEN_USER),
                verb=REPORT_ALERT,
                action_object=instance,
                level="success",
                public=False,
                description=REPORT_ALERT
            )

        else:
            if not (feedbackchanged or forwarded_for_review or rejected_report or completed):
                notify.send(
                    instance.user,
                    recipient=instance.user,
                    verb=UPDATED_VERB,
                    action_object=instance,
                    level="success",
                    public=False,
                    description="Updated Report"
                )

