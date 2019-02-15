server_status.proto
====================

.. cpp:namespace:: nvidia::inferenceserver

.. cpp:var:: message StatDuration

   Statistic collecting a duration metric.

  .. cpp:var:: uint64 count

     Cumulative number of times this metric occurred.

  .. cpp:var:: uint64 total_time_ns

     Total collected duration of this metric in nanoseconds.


.. cpp:var:: message StatusRequestStats

   Statistics collected for Status requests.

  .. cpp:var:: StatDuration success

     Total time required to handle successful Status requests, not
     including HTTP or gRPC endpoint termination time.


.. cpp:var:: message ProfileRequestStats

   Statistics collected for Profile requests.

  .. cpp:var:: StatDuration success

     Total time required to handle successful Profile requests, not
     including HTTP or gRPC endpoint termination time.


.. cpp:var:: message HealthRequestStats

   Statistics collected for Health requests.

  .. cpp:var:: StatDuration success

     Total time required to handle successful Health requests, not
     including HTTP or gRPC endpoint termination time.


.. cpp:var:: message InferRequestStats

   Statistics collected for Infer requests.

  .. cpp:var:: StatDuration success

     Total time required to handle successful Infer requests, not
     including HTTP or gRPC endpoint termination time.

  .. cpp:var:: StatDuration failed

     Total time required to handle failed Infer requests, not
     including HTTP or gRPC endpoint termination time.

  .. cpp:var:: StatDuration compute

     Time required to run inferencing for an inference request;
     including time copying input tensors to GPU memory, time
     executing the model, and time copying output tensors from GPU
     memory.

  .. cpp:var:: StatDuration queue

     Time an inference request waits in scheduling queue for an
     available model instance.


.. cpp:enum:: ModelReadyState

   Readiness status for models.

  .. cpp:enumerator:: ModelReadyState::MODEL_UNKNOWN = 0

     The model is in an unknown state. The model is not available for
     inferencing.

  .. cpp:enumerator:: ModelReadyState::MODEL_READY = 1

     The model is ready and available for inferencing.

  .. cpp:enumerator:: ModelReadyState::MODEL_UNAVAILABLE = 2

     The model is unavailable, indicating that the model failed to
     load or has been implicitly or explicitly unloaded. The model is
     not available for inferencing.

  .. cpp:enumerator:: ModelReadyState::MODEL_LOADING = 3

     The model is being loaded by the inference server. The model is
     not available for inferencing.

  .. cpp:enumerator:: ModelReadyState::MODEL_UNLOADING = 4

     The model is being unloaded by the inference server. The model is
     not available for inferencing.


.. cpp:var:: message ModelVersionStatus

   Status for a version of a model.

  .. cpp:var:: ModelReadyState ready_statue

     Current readiness state for the model.

  .. cpp:var:: map<uint32, InferRequestStats> infer_stats

     Inference statistics for the model, as a map from batch size
     to the statistics. A batch size will not occur in the map
     unless there has been at least one inference request of
     that batch size.

  .. cpp:var:: uint64 model_execution_count

     Cumulative number of model executions performed for the
     model. A single model execution performs inferencing for
     the entire request batch and can perform inferencing for multiple
     requests if dynamic batching is enabled.

  .. cpp:var:: uint64 model_inference_count

     Cumulative number of model inferences performed for the
     model. Each inference in a batched request is counted as
     an individual inference.


.. cpp:var:: message ModelStatus

   Status for a model.

  .. cpp:var:: ModelConfig config

     The configuration for the model.

  .. cpp:var:: map<int64, ModelVersionStatus> version_status

     Duration statistics for each version of the model, as a map
     from version to the status. A version will not occur in the map
     unless there has been at least one inference request of
     that model version. A version of -1 indicates the status is
     for requests for which the version could not be determined.


.. cpp:enum:: ServerReadyState

   Readiness status for the inference server.

  .. cpp:enumerator:: ServerReadyState::SERVER_INVALID = 0

     The server is in an invalid state and will likely not
     response correctly to any requests.

  .. cpp:enumerator:: ServerReadyState::SERVER_INITIALIZING = 1

     The server is initializing.

  .. cpp:enumerator:: ServerReadyState::SERVER_READY = 2

     The server is ready and accepting requests.

  .. cpp:enumerator:: ServerReadyState::SERVER_EXITING = 3

     The server is exiting and will not respond to requests.

  .. cpp:enumerator:: ServerReadyState::SERVER_FAILED_TO_INITIALIZE = 10

     The server did not initialize correctly. Most requests will fail.


.. cpp:var:: message ServerStatus

   Status for the inference server.

  .. cpp:var:: string id

     The server's ID.

  .. cpp:var:: string version

     The server's version.

  .. cpp:var:: ServerReadyState ready_state

     Current readiness state for the server.

  .. cpp:var:: uint64 uptime_ns

     Server uptime in nanoseconds.

  .. cpp:var:: map<string, ModelStatus> model_status

     Status for each model, as a map from model name to the
     status.

  .. cpp:var:: StatusRequestStats status_stats

     Statistics for Status requests.

  .. cpp:var:: ProfileRequestStats profile_stats

     Statistics for Profile requests.

  .. cpp:var:: HealthRequestStats health_stats

     Statistics for Health requests.

