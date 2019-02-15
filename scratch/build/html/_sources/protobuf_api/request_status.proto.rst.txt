request_status.proto
====================

.. cpp:namespace:: nvidia::inferenceserver

.. cpp:enum:: RequestStatusCode

   Status codes returned for inference server requests. The
   :cpp:enumerator:`RequestStatusCode::SUCCESS` status code indicates
   not error, all other codes indicate an error.

  .. cpp:enumerator:: RequestStatusCode::INVALID = 0

     Invalid status. Used internally but should not be returned as
     part of a :cpp:var:`RequestStatus`.

  .. cpp:enumerator:: RequestStatusCode::SUCCESS = 1

     Error code indicating success.

  .. cpp:enumerator:: RequestStatusCode::UNKNOWN = 2

     Error code indicating an unknown failure.

  .. cpp:enumerator:: RequestStatusCode::INTERNAL = 3

     Error code indicating an internal failure.

  .. cpp:enumerator:: RequestStatusCode::NOT_FOUND = 4

     Error code indicating a resource or request was not found.

  .. cpp:enumerator:: RequestStatusCode::INVALID_ARG = 5

     Error code indicating a failure caused by an unknown argument or
     value.

  .. cpp:enumerator:: RequestStatusCode::UNAVAILABLE = 6

     Error code indicating an unavailable resource.

  .. cpp:enumerator:: RequestStatusCode::UNSUPPORTED = 7

     Error code indicating an unsupported request or operation.


.. cpp:var:: message RequestStatus

   Status returned for all inference server requests. The
   RequestStatus provides a :cpp:enum:`RequestStatusCode`, an
   optional status message, and server and request IDs.

  .. cpp:var:: RequestStatusCode code

     The status code.

  .. cpp:var:: string msg

     The optional status message.

  .. cpp:var:: string server_id

     The identifying string for the server that is returning
     this status.

  .. cpp:var:: string request_id

     Unique identifier for the request. Value 0 (zero) indicates
     the request ID is not known.

