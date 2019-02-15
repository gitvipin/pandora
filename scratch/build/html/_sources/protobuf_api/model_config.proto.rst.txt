model_config.proto
====================

.. cpp:namespace:: nvidia::inferenceserver

.. cpp:enum:: DataType

   Data types supported for input and output tensors.

  .. cpp:enumerator:: DataType::INVALID = 0
  .. cpp:enumerator:: DataType::BOOL = 1
  .. cpp:enumerator:: DataType::UINT8 = 2
  .. cpp:enumerator:: DataType::UINT16 = 3
  .. cpp:enumerator:: DataType::UINT32 = 4
  .. cpp:enumerator:: DataType::UINT64 = 5
  .. cpp:enumerator:: DataType::INT8 = 6
  .. cpp:enumerator:: DataType::INT16 = 7
  .. cpp:enumerator:: DataType::INT32 = 8
  .. cpp:enumerator:: DataType::INT64 = 9
  .. cpp:enumerator:: DataType::FP16 = 10
  .. cpp:enumerator:: DataType::FP32 = 11
  .. cpp:enumerator:: DataType::FP64 = 12
  .. cpp:enumerator:: DataType::STRING = 13

.. cpp:var:: message ModelInstanceGroup

   A group of one or more instances of a model and resources made
   available for those instances.


  .. cpp:enum:: Kind

     Kind of this instance group.

    .. cpp:enumerator:: Kind::KIND_AUTO = 0

       This instance group represents instances that can run on either
       CPU or GPU. If all GPUs listed in 'gpus' are available then
       instances will be created on GPU(s), otherwise instances will
       be created on CPU.

    .. cpp:enumerator:: Kind::KIND_GPU = 1

       This instance group represents instances that must run on the
       GPU.

    .. cpp:enumerator:: Kind::KIND_CPU = 2

       This instance group represents instances that must run on the
       CPU.

  .. cpp:var:: string name

     Optional name of this group of instances. If not specified the
     name will be formed as <model name>_<group number>. The name of
     individual instances will be further formed by a unique instance
     number and GPU index:

  .. cpp:var:: Kind kind

     The kind of this instance group. Default is KIND_AUTO. If
     KIND_AUTO or KIND_GPU then both 'count' and 'gpu' are valid and
     may be specified. If KIND_CPU only 'count' is valid and 'gpu'
     cannot be specified.

  .. cpp:var:: int32 count

     For a group assigned to GPU, the number of instances created for
     each GPU listed in 'gpus'. For a group assigned to CPU the number
     of instances created. Default is 1.
  .. cpp:var:: int32 gpus (repeated)

     GPU(s) where instances should be available. For each GPU listed,
     'count' instances of the model will be available. Setting 'gpus'
     to empty (or not specifying at all) is eqivalent to listing all
     available GPUs.


.. cpp:var:: message ModelInput

   An input required by the model.


  .. cpp:enum:: Format

     The format for the input.

    .. cpp:enumerator:: Format::FORMAT_NONE = 0

       The input has no specific format. This is the default.

    .. cpp:enumerator:: Format::FORMAT_NHWC = 1

       HWC image format. Tensors with this format require 3 dimensions
       if the model does not support batching (max_batch_size = 0) or 4
       dimensions if the model does support batching (max_batch_size
       >= 1). In either case the 'dims' below should only specify the
       3 non-batch dimensions (i.e. HWC or CHW).

    .. cpp:enumerator:: Format::FORMAT_NCHW = 2

       CHW image format. Tensors with this format require 3 dimensions
       if the model does not support batching (max_batch_size = 0) or 4
       dimensions if the model does support batching (max_batch_size
       >= 1). In either case the 'dims' below should only specify the
       3 non-batch dimensions (i.e. HWC or CHW).

  .. cpp:var:: string name

     The name of the input.

  .. cpp:var:: DataType data_type

     The data-type of the input.

  .. cpp:var:: Format format

     The format of the input. Optional.

  .. cpp:var:: int64 dims (repeated)

     The dimensions/shape of the input tensor.


.. cpp:var:: message ModelOutput

   An output produced by the model.

  .. cpp:var:: string name

     The name of the output.

  .. cpp:var:: DataType data_type

     The data-type of the output.

  .. cpp:var:: int64 dims (repeated)

     The dimensions/shape of the output tensor.

  .. cpp:var:: string label_filename

     The label file associated with this output. Should be specified only
     for outputs that represent classifications. Optional.


.. cpp:var:: message ModelVersionPolicy

   Policy indicating which versions of a model should be made
   available by the inference server.

  .. cpp:var:: message Latest

     Serve only the latest version(s) of a model. This is
     the default policy.

    .. cpp:var:: uint32 num_versions

       Serve only the 'num_versions' highest-numbered versions. T
       The default value of 'num_versions' is 1, indicating that by
       default only the single highest-number version of a
       model will be served.

  .. cpp:var:: message All

     Serve all versions of the model.

  .. cpp:var:: message Specific

     Serve only specific versions of the model.

    .. cpp:var:: int64 versions (repeated)

       The specific versions of the model that will be served.

  .. cpp:var:: oneof policy_choice

     Each model must implement only a single version policy. The
     default policy is 'Latest'.

    .. cpp:var:: Latest latest

       Serve only latest version(s) of the model.

    .. cpp:var:: All all

       Serve all versions of the model.

    .. cpp:var:: Specific specific

       Serve only specific version(s) of the model.


.. cpp:var:: message ModelOptimizationPolicy

   Optimization settings for a model. These settings control if/how a
   model is optimized and prioritized by the backend framework when
   it is loaded.


  .. cpp:var:: message Graph

     Enable generic graph optimization of the model. If not specified
     the framework's default level of optimization is used. Currently
     only supported for TensorFlow graphdef and savedmodel models and
     causes XLA to be enabled/disabled for the model.

    .. cpp:var:: int32 level

       The optimization level. Defaults to 0 (zero) if not specified.

         - -1: Disabled
         -  0: Framework default
         -  1+: Enable optimization level (greater values indicate
            higher optimization levels)


  .. cpp:enum:: ModelPriority

     Model priorities. A model will be given scheduling and execution
     preference over models at lower priorities. Current model
     priorities only work for TensorRT models.

    .. cpp:enumerator:: ModelPriority::PRIORITY_DEFAULT = 0

       The default model priority.

    .. cpp:enumerator:: ModelPriority::PRIORITY_MAX = 1

       The maximum model priority.

    .. cpp:enumerator:: ModelPriority::PRIORITY_MIN = 2

       The minimum model priority.

  .. cpp:var:: Graph graph

     The graph optimization setting for the model. Optional.

  .. cpp:var:: ModelPriority priority

     The priority setting for the model. Optional.


.. cpp:var:: message ModelDynamicBatching

   Dynamic batching configuration. These settings control how dynamic
   batching operates for the model.

  .. cpp:var:: int32 preferred_batch_size (repeated)

     Preferred batch sizes for dynamic batching. If a batch of one of
     these sizes can be formed it will be executed immediately.  If
     not specified a preferred batch size will be chosen automatically
     based on model and GPU characteristics.

  .. cpp:var:: int32 max_queue_delay_microseconds

     The maximum time, in microseconds, a request will be delayed in
     the scheduling queue to wait for additional requests for
     batching. Default is 0.


.. cpp:var:: message ModelSequenceBatching

   Sequence batching configuration. These settings control how sequence
   batching operates for the model.

  .. cpp:var:: uint32 max_queue_delay_microseconds

     The maximum time, in microseconds, a request will be delayed in
     the scheduling queue to wait for additional requests for
     batching. Default is 0.

  .. cpp:var:: message Control

     A control is a binary signal to a backend.


    .. cpp:enum:: Kind

       The kind of the control.

      .. cpp:enumerator:: Kind::CONTROL_SEQUENCE_START = 0

         A new sequence is/is-not starting. If true a sequence is
         starting, if false a sequence is continuing.

      .. cpp:enumerator:: Kind::CONTROL_SEQUENCE_READY = 1

         A sequence is/is-not ready for inference. If true the
         input tensor data is valid and should be used. If false
         the input tensor data is invalid and inferencing should
         be "skipped".

    .. cpp:var:: Kind kind

       The kind of this control.

    .. cpp:var:: int32 int32_false_true (repeated)

       The control's true and false setting is indicated by setting
       an int32 value in a tensor. The tensor must be a
       1-dimensional tensor with size equal to the batch size of
       the request. 'int32_false_true' must have two entries: the
       first the false value and the second the true value.

  .. cpp:var:: message ControlInput

     The sequence control values to communicate by a model input.

    .. cpp:var:: string name

       The name of the model input.

    .. cpp:var:: Control control (repeated)

       The control value(s) that should be communicated to the
       model using this model input.

  .. cpp:var:: ControlInput control_input (repeated)

     The model input(s) that the server should use to communicate
     sequence start, stop, ready and similar control values to the
     model.


.. cpp:var:: message ModelConfig

   A model configuration.

  .. cpp:var:: string name

     The name of the model.

  .. cpp:var:: string platform

     The framework for the model. Possible values are
     "tensorrt_plan", "tensorflow_graphdef",
     "tensorflow_savedmodel", and "caffe2_netdef".

  .. cpp:var:: ModelVersionPolicy version_policy

     Policy indicating which version(s) of the model will be served.

  .. cpp:var:: int32 max_batch_size

     Maximum batch size allowed for inference. This can only decrease
     what is allowed by the model itself. A max_batch_size value of 0
     indicates that batching is not allowed for the model and the
     dimension/shape of the input and output tensors must exactly
     match what is specified in the input and output configuration. A
     max_batch_size value > 0 indicates that batching is allowed and
     so the model expects the input tensors to have an additional
     initial dimension for the batching that is not specified in the
     input (for example, if the model supports batched inputs of
     2-dimensional tensors then the model configuration will specify
     the input shape as [ X, Y ] but the model will expect the actual
     input tensors to have shape [ N, X, Y ]). For max_batch_size > 0
     returned outputs will also have an additional initial dimension
     for the batch.

  .. cpp:var:: ModelInput input (repeated)

     The inputs request by the model.

  .. cpp:var:: ModelOutput output (repeated)

     The outputs produced by the model.

  .. cpp:var:: ModelOptimizationPolicy optimization

     Optimization configuration for the model. If not specified
     then default optimization policy is used.

  .. cpp:var:: oneof scheduling_choice

     The scheduling policy for the model. If not specified the
     default scheduling policy is used for the model. The default
     policy is to execute each inference request independently.

    .. cpp:var:: ModelDynamicBatching dynamic_batching

       If specified, enables the dynamic-batching scheduling
       policy. With dynamic-batching the scheduler may group
       together independent requests into a single batch to
       improve inference throughput.

    .. cpp:var:: ModelSequenceBatching sequence_batching

       If specified, enables the sequence-batching scheduling
       policy. With sequence-batching, inference requests
       with the same correlation ID are routed to the same
       model instance. Multiple sequences of inference requests
       may be batched together into a single batch to
       improve inference throughput.

  .. cpp:var:: ModelInstanceGroup instance_group (repeated)

     Instances of this model. If not specified, one instance
     of the model will be instantiated on each available GPU.

  .. cpp:var:: string default_model_filename

     Optional filename of the model file to use if a
     compute-capability specific model is not specified in
     :cpp:var:`cc_model_names`. If not specified the default name
     is 'model.graphdef', 'model.savedmodel', 'model.plan' or
     'model.netdef' depending on the model type.

  .. cpp:var:: map<string,string> cc_model_filenames

     Optional map from CUDA compute capability to the filename of
     the model that supports that compute capability. The filename
     refers to a file within the model version directory.

  .. cpp:var:: map<string,string> tags

     Optional model tags. User-specific key-value pairs for this
     model. These tags are applied to the metrics reported on the HTTP
     metrics port.

