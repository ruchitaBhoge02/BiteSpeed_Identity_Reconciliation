from core.db_utils.sqlite_utils import ContactService

contact_service = ContactService()
# Main identify function that processes the incoming data
def identify(data):
    try:
        email = data.get('email')
        phone_number = data.get('phoneNumber')

        # Find existing contacts based on provided email or phone number
        existing_contacts = contact_service.find_existing_contacts(email, phone_number)

        if existing_contacts:
            # Consolidate contacts if existing contacts are found
            return {
                "contact": contact_service.consolidate_contacts(existing_contacts, email, phone_number)
            }
        else:
            # Create a new primary contact if no existing contacts are found
            new_contact = contact_service.create_primary_contact(email, phone_number)
            return {
                "contact": {
                    "primaryContatctId": new_contact.id,
                    "emails": [email] if email else [],
                    "phoneNumbers": [phone_number] if phone_number else [],
                    "secondaryContactIds": []
                }
            }
    except Exception as e:
        print(f"Error identifying contact: {e}")
        return {
            "contact": {
                "primaryContatctId": None,
                "emails": [],
                "phoneNumbers": [],
                "secondaryContactIds": []
            }
        }
