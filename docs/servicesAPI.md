# Services API endpoints

Documentation for the REST API.


## Classify Service

**URI**: `http://host:port/services/classify/{PLUGIN_NAME}`

Where `{PLUGIN_NAME}` is one of the supported plugin names, otherwise an error will be raised.

One of either `imagePath` or `imageFile` are required.

* **Method**: _POST_
* **URL Query Parameters**: 
    * No parameters.
* **Fields**:
    * _Required_:
        * None
    * _Optional_:
        * imagePath: Path to image on the server's file system.
        * imageFile: Data uploaded with a upload request. This should be a `file` attribute containing the image.
        * x: X co-ordinate of an chosen point on the image. Integer from 0 (left) to 100 (right) as a percentage value (not pixels).
        * y: Y co-ordinate of an chosen point on the image. Integer from 0 (top) to 100 (bottom) as a percentage value (not pixels).
* **Reply on success**:
    * Return an HTTP 201 status and the response data for the classifier plugin in the following format:
        
        ```
        [
            string,
            string,
            ...
        ]
        ```
