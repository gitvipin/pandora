
.. _program_listing_file_src_servables_custom_custom.h:

Program Listing for File custom.h
=================================

|exhale_lsh| :ref:`Return to documentation for file <file_src_servables_custom_custom.h>` (``src/servables/custom/custom.h``)

.. |exhale_lsh| unicode:: U+021B0 .. UPWARDS ARROW WITH TIP LEFTWARDS

.. code-block:: cpp

   // Copyright (c) 2018-2019, NVIDIA CORPORATION. All rights reserved.
   //
   // Redistribution and use in source and binary forms, with or without
   // modification, are permitted provided that the following conditions
   // are met:
   //  * Redistributions of source code must retain the above copyright
   //    notice, this list of conditions and the following disclaimer.
   //  * Redistributions in binary form must reproduce the above copyright
   //    notice, this list of conditions and the following disclaimer in the
   //    documentation and/or other materials provided with the distribution.
   //  * Neither the name of NVIDIA CORPORATION nor the names of its
   //    contributors may be used to endorse or promote products derived
   //    from this software without specific prior written permission.
   //
   // THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
   // EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   // IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
   // PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
   // CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   // EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   // PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
   // PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
   // OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   // (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   // OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
   #pragma once
   
   #include <stddef.h>
   #include <stdint.h>
   
   #ifdef __cplusplus
   extern "C" {
   #endif
   
   #define CUSTOM_NO_GPU_DEVICE -1
   
   // A payload represents the input tensors and the required output
   // needed for execution in the backend.
   typedef struct custom_payload_struct {
     // The size of the batch represented by this payload.
     uint32_t batch_size;
   
     // The number of inputs included in this payload.
     uint32_t input_cnt;
   
     // The 'input_cnt' names of the inputs included in this payload.
     const char** input_names;
   
     // For each of the 'input_cnt' inputs, the number of dimensions in
     // the input's shape, not including the batch dimension.
     const size_t* input_shape_dim_cnts;
   
     // For each of the 'input_cnt' inputs, the shape of the input, not
     // including the batch dimension.
     const int64_t** input_shape_dims;
   
     // The number of outputs that must be computed for this payload. Can
     // be 0 to indicate that no outputs are required from the backend.
     uint32_t output_cnt;
   
     // The 'output_cnt' names of the outputs that must be computed for
     // this payload. Each name must be one of the names from the model
     // configuration, but all outputs do not need to be computed.
     const char** required_output_names;
   
     // The context to use with CustomGetNextInput callback function to
     // get the input tensor values for this payload.
     void* input_context;
   
     // The context to use with CustomGetOutput callback function to get
     // the buffer for output tensor values for this payload.
     void* output_context;
   
     // The error code indicating success or failure from execution. A
     // value of 0 (zero) indicates success, all other values indicate
     // failure and are backend defined.
     int error_code;
   } CustomPayload;
   
   typedef bool (*CustomGetNextInputFn_t)(
       void* input_context, const char* name, const void** content,
       uint64_t* content_byte_size);
   
   typedef bool (*CustomGetOutputFn_t)(
       void* output_context, const char* name, size_t shape_dim_cnt,
       int64_t* shape_dims, uint64_t content_byte_size, void** content);
   
   typedef int (*CustomInitializeFn_t)(const char*, size_t, int, void**);
   
   typedef int (*CustomFinalizeFn_t)(void*);
   
   typedef char* (*CustomErrorStringFn_t)(void*, int);
   
   typedef int (*CustomExecuteFn_t)(
       void*, uint32_t, CustomPayload*, CustomGetNextInputFn_t,
       CustomGetOutputFn_t);
   
   int CustomInitialize(
       const char* serialized_model_config, size_t serialized_model_config_size,
       int gpu_device_id, void** custom_context);
   
   int CustomFinalize(void* custom_context);
   
   const char* CustomErrorString(void* custom_context, int errcode);
   
   int CustomExecute(
       void* custom_context, uint32_t payload_cnt, CustomPayload* payloads,
       CustomGetNextInputFn_t input_fn, CustomGetOutputFn_t output_fn);
   
   #ifdef __cplusplus
   }
   #endif
