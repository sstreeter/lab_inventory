export_templates.py
import csv
import io

def export_inventory_csv(items, export_type='sn_asset'):
    output = io.StringIO()
    writer = csv.writer(output)
        
    if export_type == 'sn_asset':
        writer.writerow(['Device Name', 'Serial Number', 'Lab'])
        for item in items:
            writer.writerow([item.device_name, item.serial_number, item.lab])
    else:
        writer.writerow(['ID', 'Device Name', 'Serial Number', 'Lab', 'Image Path'])
        for item in items:
            writer.writerow([item.id, item.device_name, item.serial_number, item.lab, item.image_path])
    
    return output.getvalue()
