CITIZEN_USER = 1
DATA_ENTRANT = 2
MANAGER_TRANSPORT = 3
DEPUTY_DIRECTOR_TRANSPORT = 4

USER_ROLE_TYPES = (
    (CITIZEN_USER, "Citizen/General Public"),
    (DATA_ENTRANT, "Data Entrant/Officer Transport"),
    (DEPUTY_DIRECTOR_TRANSPORT, "Deputy Director Transport"),
    (MANAGER_TRANSPORT, "Manager Transport")
)

GENDER_MALE = "male"
GENDER_FEMALE = "female"

GENDER_CHOICES = (
    (GENDER_MALE,"Male"),
    (GENDER_FEMALE,"Female")
)

NATIONALITY_UG = 1
NATIONALITY_UG_NONE = 0

NATIONALITY_CHOICES = (
    (NATIONALITY_UG,"Ugandan"),
    (NATIONALITY_UG_NONE, "Non Uganda")
)

NIN_FIELD_LENGTH = 14
VALIDATION_CODE_LENGTH = 5

PENDING_OTP = "pending"
CONFIRMED_OTP =  "confirmed"

EMERGENCY_INCIDENT = 1
NON_EMERGENCY_INCIDENT = 2

EMERGENCY_CHOICES = (
    (EMERGENCY_INCIDENT, "Emergency"),
    (NON_EMERGENCY_INCIDENT, "Non-Emergency")
)

INCIDENT_STATUS_PENDING = "pending"
INCIDENT_STATUS_FOR_REVIEW = "for_review"
INCIDENT_STATUS_COMPLETE = "complete"