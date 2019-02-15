api.proto
====================

.. cpp:namespace:: nvidia::inferenceserver

.. cpp:var:: message InferRequestHeader

   Meta-data for an inferencing request. The actual input data is
   delivered separate from this header, in the HTTP body for an HTTP
   request, or in the :cpp:var:`InferRequest` message for a gRPC request.

  .. cpp:enum:: Flag

     Flags that can be associated with an inference request.
     All flags are packed bitwise into the 'flags' field and
     so the value of each must be a power-of-2.

    .. cpp:enumerator:: Flag::FLAG_NONE = 0

       Value indicating no flags are enabled.

    .. cpp:enumerator:: Flag::FLAG_SEQUENCE_END = 1

       This request is the end of a related sequence of requests.

  .. cpp:var:: message Input

     Meta-data for an input tensor provided as part of an inferencing
     request.

    .. cpp:var:: string name

       The name of the input tensor.

    .. cpp:var:: int64 dims (repeated)

       The shape of the input tensor, not including the batch dimension.
       Optional if the model configuration for this input explicitly
       specifies all dimensions of the shape. Required if the model
       configuration for this input has any wildcard dimensions (-1).

    .. cpp:var:: uint64 batch_byte_size

       The size of the full batch of the input tensor, in bytes.
       Optional for tensors with fixed-sized datatypes. Required
       for tensors with a non-fixed-size datatype (like STRING).

  .. cpp:var:: message Output

     Meta-data for a requested output tensor as part of an inferencing
     request.

    .. cpp:var:: string name

       The name of the output tensor.

    .. cpp:var:: message Class

       Options for an output returned as a classification.

      .. cpp:var:: uint32 count

         Indicates how many classification values should be returned
         for the output. The 'count' highest priority values are
         returned.

    .. cpp:var:: Class cls

       Optional. If defined return this output as a classification
       instead of raw data. The output tensor will be interpreted as
       probabilities and the classifications associated with the
       highest probabilities will be returned.

  .. cpp:var:: uint64 id

     The ID of the inference request. The response of the request will
     have the same ID in InferResponseHeader. The request sender can use
     the ID to correlate the response to corresponding request if needed.

  .. cpp:var:: uint32 flags

     The flags associated with this request. This field holds a bitwise-or
     of all flag values.

  .. cpp:var:: uint64 correlation_id

     The correlation ID of the inference request. Default is 0, which
     indictes that the request has no correlation ID. The correlation ID
     is used to indicate two or more inference request are related to
     each other. How this relationship is handled by the inference
     server is determined by the model's scheduling policy.

  .. cpp:var:: uint32 batch_size

     The batch size of the inference request. This must be >= 1. For
     models that don't support batching, batch_size must be 1.

  .. cpp:var:: Input input (repeated)

     The input meta-data for the inputs provided with the the inference
     request.

  .. cpp:var:: Output output (repeated)

     The output meta-data for the inputs provided with the the inference
     request.


.. cpp:var:: message InferResponseHeader

   Meta-data for the response to an inferencing request. The actual output
   data is delivered separate from this header, in the HTTP body for an HTTP
   request, or in the :cpp:var:`InferResponse` message for a gRPC request.

  .. cpp:var:: message Output

     Meta-data for an output tensor requested as part of an inferencing
     request.

    .. cpp:var:: string name

       The name of the output tensor.

    .. cpp:var:: message Raw

       Meta-data for an output tensor being returned as raw data.

      .. cpp:var:: int64 dims (repeated)

         The shape of the output tensor, not including the batch
         dimension.

      .. cpp:var:: uint64 batch_byte_size

         The full size of the output tensor, in bytes. For a
         batch output, this is the size of the entire batch.

    .. cpp:var:: message Class

       Information about each classification for this output.

      .. cpp:var:: int32 idx

         The classification index.

      .. cpp:var:: float value

         The classification value as a float (typically a
         probability).

      .. cpp:var:: string label

         The label for the class (optional, only available if provided
         by the model).

    .. cpp:var:: message Classes

       Meta-data for an output tensor being returned as classifications.

      .. cpp:var:: Class cls (repeated)

         The topk classes for this output.

    .. cpp:var:: Raw raw

       If specified deliver results for this output as raw tensor data.
       The actual output data is delivered in the HTTP body for an HTTP
       request, or in the :cpp:var:`InferResponse` message for a gRPC
       request. Only one of 'raw' and 'batch_classes' may be specified.

    .. cpp:var:: Classes batch_classes (repeated)

       If specified deliver results for this output as classifications.
       There is one :cpp:var:`Classes` object for each batch entry in
       the output. Only one of 'raw' and 'batch_classes' may be
       specified.

  .. cpp:var:: uint64 id

     The ID of the inference response. The response will have the same ID
     as the ID of its originated request. The request sender can use
     the ID to correlate the response to corresponding request if needed.

  .. cpp:var:: string model_name

     The name of the model that produced the outputs.

  .. cpp:var:: int64 model_version

     The version of the model that produced the outputs.

  .. cpp:var:: uint32 batch_size

     The batch size of the outputs. This will always be equal to the
     batch size of the inputs. For models that don't support
     batching the batch_size will be 1.

  .. cpp:var:: Output output (repeated)

     The outputs, in the same order as they were requested in
     :cpp:var:`InferRequestHeader`.

