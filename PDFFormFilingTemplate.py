import datetime
import os
from fillpdf import fillpdfs
import pandas as pd

# Load the districts CSV
df = pd.read_csv("DistrictsWEwant.csv")

# Create output directory if it doesn't exist
output_dir = "settlementPDFS"
os.makedirs(output_dir, exist_ok=True)

# Get list of form fields
form_fields = list(fillpdfs.get_form_fields("RTKRequestForm.pdf").keys())

# Static info
full_name = "My Name"
company = "My Organization"
email = "My Email Address"
address = "123 Paper Street"
city = "Dallastown"
state = "PA"
zipcode = "99999"
date_today = datetime.date.today().strftime("%B %d, %Y")
phone_number = '867-555-5309'

records_requested = (
    "I am requesting a list of all settlements involving the school district and the corresponding amount of the settlement (if any) "
    "for school years 2018/19-present. If a list does not exist and the district is unable to create one, "
    "I am requesting copies of individual settlement agreements involving the school district for the school years 2018/19-present. "
    "I am not seeking student identity information and do not object to its redaction if it appears in settlement agreements."
)

# Iterate over each district
for district_name in df["District"]:
    # Build the data dictionary
    data_dict = {
        form_fields[0]: district_name,
        form_fields[1]: date_today,
        form_fields[2]: "On",         # Email submission method
        form_fields[6]: full_name,
        form_fields[7]: company,
        form_fields[8]: "On",         # Preferred contact: Email
        form_fields[10]: email,
        form_fields[11]: address,
        form_fields[12]: city,
        form_fields[13]: state,
        form_fields[14]: zipcode,
        form_fields[15]: phone_number,
        form_fields[17]: "On",
        form_fields[19]: "On",# Confirm Email contact again if needed
        form_fields[20]: records_requested,
        form_fields[23]: "On",        # Request electronic copies
        form_fields[26]: "On",        # Acknowledge fees
        form_fields[27]: "20",        # Notify if fees exceed $20
        form_fields[29]: "On",        # No certified copies
    }

    # Clean and shorten district name for filename
    short_district = district_name.replace(" Area School District", "").replace(" School District", "")
    clean_district = short_district.replace("/", "-").replace(" ", "_")
    output_filename = f"{clean_district}_settlement_-_{full_name}.pdf"
    output_path = os.path.join(output_dir, output_filename)

    # Write filled form
    fillpdfs.write_fillable_pdf("RTKRequestForm.pdf", output_path, data_dict=data_dict)

print(f"✅ All PDFs written to: {output_dir}/")
