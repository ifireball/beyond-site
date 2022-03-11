"""Mail sending protocols"""

from abc import abstractmethod
from typing import Protocol

from ..models import Certificate, MailJob


class MailJobRunner(Protocol):
    """Takes care of sending certificates via email"""

    @abstractmethod
    def __call__(self, mail_job: MailJob) -> None:
        """Send the certificates linked to the given MailJob"""


class CertificateMailSender(Protocol):
    """Sends a particular certificate via email"""

    @abstractmethod
    def __call__(self, mail_job: MailJob, certificate: Certificate) -> None:
        """Send the provided certificate via email"""
