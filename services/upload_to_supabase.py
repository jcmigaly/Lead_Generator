import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

def upload_contractors():
    """Upload contractors data to Supabase"""
    try:
        # Read the contractors data
        with open('contractors_data.json', 'r') as file:
            contractors = json.load(file)
        
        print(f"Found {len(contractors)} contractors to upload")
        
        # Upload each contractor
        for contractor in contractors:
            # Prepare the data structure according to your Supabase table schema
            contractor_data = {
                'name': contractor['name'],
                'phone': contractor['phone'],
                'address': contractor['address'],
                'rating': contractor['rating'],
                'certifications': contractor['certifications'],
                'services': contractor['services'],
                'about': contractor['about'],
                'insight': contractor['insight'],
                'profile_url': contractor['url']
            }
            
            # Insert the data into your Supabase table
            result = supabase.table('contractors').insert(contractor_data).execute()
            
            # Check if the insertion was successful
            if hasattr(result, 'data'):
                print(f"Successfully uploaded {contractor['name']}")
            else:
                print(f"Failed to upload {contractor['name']}")
                
        print("Upload completed!")
        
    except Exception as e:
        print(f"Error during upload: {e}")

if __name__ == "__main__":
    upload_contractors() 