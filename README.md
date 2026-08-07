# funko_tracker
Android app tracker








Flowchart: Manual Funko Entry Screen
====================================

User fills out the form
        |
        v
+---------------------------+
| validate_form()           |
+---------------------------+
        |
  Are there errors?
    /       \
   Yes       No
   |         |
   v         v
show_errors()  process_form()
   |             |
   |        Prepare payload:
   |        {
   |          "name": ...,
   |          "license": ...,
   |          "barcode": ...,
   |          "number": ...
   |        }
   |             |
   |             v
   |        post_funko(payload)  (in a background thread)
   |             |
   |       API call to FUNKO_ENDPOINT
   |             |
   |     +-------+--------+
   |     |                |
   |   Success          Failure
   | (200/201)         (other or network error)
   |     |                |
   v     v                v
Snackbar: "Funko added 🎉"   Snackbar: "API Error"
   |                         (or Status Code)
   v
redirect_to_home() → Home screen
