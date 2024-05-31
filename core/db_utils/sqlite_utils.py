from core.db_utils.database_init import db, Contact
from sqlalchemy.exc import SQLAlchemyError


class ContactService:
    # Find existing contacts based on email or phoneNumber
    @staticmethod
    def find_existing_contacts(email, phone_number):
        try:
            return Contact.query.filter(
                (Contact.email == email) | (Contact.phone_number == phone_number)
            ).all()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    # Create a new secondary contact linked to the primary contact
    @staticmethod
    def create_secondary_contact(primary_contact, email, phone_number):
        try:
            new_contact = Contact(
                email=email,
                phone_number=phone_number,
                linked_id=primary_contact.id,
                link_precedence='secondary'
            )
            db.session.add(new_contact)
            db.session.commit()
            return new_contact
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()
            return None

    # Create a new primary contact
    @staticmethod
    def create_primary_contact(email, phone_number):
        try:
            new_contact = Contact(
                email=email,
                phone_number=phone_number,
                link_precedence='primary'
            )
            db.session.add(new_contact)
            db.session.commit()
            return new_contact
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            db.session.rollback()
            return None

    # Consolidate existing contacts and add new contact information if necessary
    @staticmethod
    def consolidate_contacts(existing_contacts, email, phone_number):
        try:
            # Find the primary contact (oldest contact)
            primary_contact = min(existing_contacts, key=lambda c: c.created_at)
            emails = set()
            phone_numbers = set()
            secondary_contacts = []

            # Initialize sets for emails and phoneNumbers
            for contact in existing_contacts:
                if contact.link_precedence == 'primary':
                    primary_contact = contact
                else:
                    secondary_contacts.append(contact.id)

                if contact.email:
                    emails.add(contact.email)
                if contact.phone_number:
                    phone_numbers.add(contact.phone_number)

            # Add new email as a secondary contact if it's not already present
            if email and email not in emails:
                new_contact = ContactService.create_secondary_contact(primary_contact, email, phone_number)
                if new_contact:
                    secondary_contacts.append(new_contact.id)
                    emails.add(email)

            # Add new phone number as a secondary contact if it's not already present
            if phone_number and phone_number not in phone_numbers:
                new_contact = ContactService.create_secondary_contact(primary_contact, email, phone_number)
                if new_contact:
                    secondary_contacts.append(new_contact.id)
                    phone_numbers.add(phone_number)

            return {
                "primaryContatctId": primary_contact.id,
                "emails": list(emails),
                "phoneNumbers": list(phone_numbers),
                "secondaryContactIds": secondary_contacts
            }
        except Exception as e:
            print(f"Error consolidating contacts: {e}")
            return {
                "primaryContatctId": None,
                "emails": [],
                "phoneNumbers": [],
                "secondaryContactIds": []
            }
