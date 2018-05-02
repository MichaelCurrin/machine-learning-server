# API endpoints

Documentation for the REST API.

With the default configuration, use the following values:

* host: `localhost`
* port: `9000`


## Web app

The application's HTML files in the [static directory](/mlserver/static) can be accessed off the root path as:

- `http://host:port/` OR `http://host:port/index.html`
- `http://host:port/classify/builtinColors.html`
- `http://host:port/classify/dropinColors.html`


## Services endpoint

**URI**: `http://host:port/services/`

This serves as a root for all REST services.

* **Method**: _GET_
* **URL Query Parameters**:
    * No parameters.
* **Fields**:
    * _Required_:
        * None
    * _Optional_:
        * None
* **Reply on failure**:
    * Return an HTTP _404_ status.


## Classify endpoint

**URI**: `http://host:port/services/classify`

* **Method**: _GET_
* **URL Query Parameters**:
    * No parameters.
* **Fields**:
    * _Required_:
        * None
    * _Optional_:
        * None
* **Reply on success**:
    * Return an HTTP _400_ status and a dictionary response including valid plugin names can be used on the [Plugin endpoint](#plugin-endpoint) classify service.


## Plugin endpoint

**URI**: `http://host:port/services/classify/{PLUGIN_NAME}`

Where `{PLUGIN_NAME}` is one of the supported plugin names (see [Classify](#classify-endpoint) endpoint).

One of either `imagePath` or `imageFile` are required.

* **Method**: _POST_
* **URL Query Parameters**:
    * No parameters.
* **Fields**:
    * _Required_:
        * None
    * _Optional_:
        * imagePath: Path to image on the server's file system.
        * imageFile: Data uploaded with a upload request. This should be a multi-part upload with a `file` attribute containing the image data.
        * x: The X co-ordinate of an chosen point on the image. Integer from 0 (left) to 100 (right) as a percentage value (not pixels).
        * y: The Y co-ordinate of an chosen point on the image. Integer from 0 (top) to 100 (bottom) as a percentage value (not pixels).
* **Reply on success**:
    * Return an HTTP _201_ status and the response data for the classifier plugin in the following format:
        
        ```
        [
            string,
            string,
            ...
        ]
        ```

* **Reply on failure**:
    * Return an HTTP _400_ status if the plugin name given is not valid or the plugin is incorrectly configured.
