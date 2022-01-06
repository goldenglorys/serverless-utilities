from .utilities import Utilities
from http.server import BaseHTTPRequestHandler
import json
import googleapiclient
from datetime import datetime


class RappiReworkApi(Utilities):

    def process_sheet(self, link, tab_name, batch_name):
        valid_link = False
        sheet_exists = True
        has_permission = True
        tab_exists = False
        valid_header_format = False
        import_reworks = False
        try:
            sheet_id = link.split("/")[5]
            valid_link = True
            data = self.get_sheet_meta_data(
                sheet_id
            )
            summary_meta_data = {
                "title": data["properties"]["title"],
                "tabs":[el["properties"]["title"] for el in data['sheets']]
            }
            tab_exists = any(ele==tab_name for ele in summary_meta_data['tabs'])
            sheet_data = self.get_sheet(
                sheet_id,
               "'"+tab_name+"'!A:O"
            )
            header_row = [x.strip() for x in sheet_data["values"][0]]
            true_header_row = ['Store ID', 'Rework Reason', 'Status']
            if header_row == true_header_row:
                valid_header_format = True
            if tab_exists and valid_header_format:
                rows = self.read_sheet(sheet_id, tab_name)
                for row in range(len(rows)):
                    result = self.check_if_store_exist(rows[row][0])
                    if len(result) == 1:
                        rows[row][2] = 'Sent to Rework'
                        self.update_rework_row(
                            result[0]['id'],
                            batch_name,
                            rows[row][1],
                            True,
                            'New'
                        )
                    else:
                        rows[row][2] = 'Not Found'
                rows.insert(0, true_header_row)
                update_sheet = self.update_sheet(sheet_id, "'"+tab_name+"'!A:O", rows)
                if update_sheet:
                    import_reworks = True
        except googleapiclient.errors.HttpError as err:
            if err.resp.status == 404:
                sheet_exists = False
                has_permission = False
            elif err.resp.status == 403:
                has_permission = False
        return {
            "valid_link": valid_link,
            "has_permission": has_permission,
            "sheet_exists": sheet_exists,
            "tab_exists": tab_exists,
            "valid_header_format": valid_header_format,
            "import_reworks": import_reworks
        }


    def read_sheet(self, sheet_id, tab_name):
        sheet_data = self.get_sheet(sheet_id,"'"+tab_name+"'!A:O")
        return sheet_data['values'][1:]


    def check_if_store_exist(self, store_id):
        sql = f"""
            SELECT id, client_store_id FROM rappi.le_upload 
            WHERE client_store_id = '{store_id}'
        """
        db_result = self.run_simple_sql_query(sql)
        return db_result


    def update_rework_row(self, id, rework_batch, rework_reason, rework_flag, rework_status):
        sql = f"""
            UPDATE rappi.le_upload
                SET
                    rework_flag = {rework_flag},
                    rework_batch = '{rework_batch}',
                    rework_status = '{rework_status}',
                    rework_reason = '{rework_reason}'
            WHERE id = {id} RETURNING id
        """
        self.run_simple_sql_query(sql)
        

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(content_len))
        d = RappiReworkApi()
        processing_result = d.process_sheet(
            post_data['sheet_url'],
            post_data['tab_name'],
            post_data['batch_name'],
        )
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin",
                         "https://flow.inv.tech/")
        self.end_headers()
        self.wfile.write(
            json.dumps(processing_result).encode()
        )