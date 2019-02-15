grpc_service.proto
====================

.. cpp:namespace:: nvidia::inferenceserver

.. cpp:var:: service GRPCService

   Inference Server GRPC endpoints.

  .. cpp:var:: rpc Status(StatusRequest) returns (StatusResponse)

     Get status for entire inference server or for a specified model.

  .. cpp:var:: rpc Profile(ProfileRequest) returns (ProfileResponse)

     Enable and disable low-level GPU profiling.

  .. cpp:var:: rpc Health(HealthRequest) returns (HealthResponse)

     Check liveness and readiness of the inference server.

  .. cpp:var:: rpc Infer(InferRequest) returns (InferResponse)

     Request inference using a specific model. [ To handle large input
     tensors likely need to set the maximum message size to that they
     can be transmitted in one pass.

  .. cpp:var:: rpc StreamInfer(stream InferRequest) returns (stream
     InferResponse)

     Request inferences using a specific model in a streaming manner.
     Individual inference requests sent through the same stream will be
     processed in order and be returned on completion


.. cpp:var:: message StatusRequest

   Request message for Status gRPC endpoint.


  .. cpp:var:: string model_name

     The specific model status to be returned. If empty return status
     for all models.


.. cpp:var:: message StatusResponse

   Response message for Status gRPC endpoint.


  .. cpp:var:: RequestStatus request_status

     The status of the request, indicating success or failure.


  .. cpp:var:: ServerStatus server_status

     The server and model status.


.. cpp:var:: message ProfileRequest

   Request message for Profile gRPC endpoint.


  .. cpp:var:: string cmd

     The requested profiling action: 'start' requests that GPU
     profiling be enabled on all GPUs controlled by the inference
     server; 'stop' requests that GPU profiling be disabled on all GPUs
     controlled by the inference server.


.. cpp:var:: message ProfileResponse

   Response message for Profile gRPC endpoint.


  .. cpp:var:: RequestStatus request_status

     The status of the request, indicating success or failure.


.. cpp:var:: message HealthRequest

   Request message for Health gRPC endpoint.


  .. cpp:var:: string mode

     The requested health action: 'live' requests the liveness
     state of the inference server; 'ready' requests the readiness state
     of the inference server.


.. cpp:var:: message HealthResponse

   Response message for Health gRPC endpoint.


  .. cpp:var:: RequestStatus request_status

     The status of the request, indicating success or failure.


  .. cpp:var:: bool health

     The result of the request. True indicates the inference server is
     live/ready, false indicates the inference server is not live/ready.


.. cpp:var:: message InferRequest

   Request message for Infer gRPC endpoint.

  .. cpp:var:: string model_name

     The name of the model to use for inferencing.

  .. cpp:var:: int64 version

     The version of the model to use for inference. If -1
     the latest/most-recent version of the model is used.

  .. cpp:var:: InferRequestHeader meta_data

     Meta-data for the request profiling input tensors and requesting
     output tensors.

  .. cpp:var:: bytes raw_input (repeated)

     The raw input tensor data in the order specified in 'meta_data'.


.. cpp:var:: message InferResponse

   Response message for Infer gRPC endpoint.


  .. cpp:var:: RequestStatus request_status

     The status of the request, indicating success or failure.

  .. cpp:var:: InferResponseHeader meta_data

     The response meta-data for the output tensors.

  .. cpp:var:: bytes raw_output (repeated)

     The raw output tensor data in the order specified in 'meta_data'.

