
.. _program_listing_file_src_clients_c++_request.h:

Program Listing for File request.h
==================================

|exhale_lsh| :ref:`Return to documentation for file <file_src_clients_c++_request.h>` (``src/clients/c++/request.h``)

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
   
   
   #include <curl/curl.h>
   #include <grpcpp/grpcpp.h>
   #include <condition_variable>
   #include <memory>
   #include <mutex>
   #include <string>
   #include <thread>
   #include <vector>
   #include "src/core/api.pb.h"
   #include "src/core/grpc_service.grpc.pb.h"
   #include "src/core/grpc_service.pb.h"
   #include "src/core/model_config.h"
   #include "src/core/model_config.pb.h"
   #include "src/core/request_status.pb.h"
   #include "src/core/server_status.pb.h"
   
   namespace nvidia { namespace inferenceserver { namespace client {
   
   //==============================================================================
   class Error {
    public:
     explicit Error(const RequestStatus& status);
   
     explicit Error(RequestStatusCode code = RequestStatusCode::SUCCESS);
   
     explicit Error(RequestStatusCode code, const std::string& msg);
   
     RequestStatusCode Code() const { return code_; }
   
     const std::string& Message() const { return msg_; }
   
     const std::string& ServerId() const { return server_id_; }
   
     uint64_t RequestId() const { return request_id_; }
   
     bool IsOk() const { return code_ == RequestStatusCode::SUCCESS; }
   
     static const Error Success;
   
    private:
     friend std::ostream& operator<<(std::ostream&, const Error&);
     RequestStatusCode code_;
     std::string msg_;
     std::string server_id_;
     uint64_t request_id_;
   };
   
   //==============================================================================
   class ServerHealthContext {
    public:
     virtual Error GetReady(bool* ready) = 0;
   
     virtual Error GetLive(bool* live) = 0;
   
    protected:
     ServerHealthContext(bool);
   
     // If true print verbose output
     const bool verbose_;
   };
   
   //==============================================================================
   class ServerStatusContext {
    public:
     virtual Error GetServerStatus(ServerStatus* status) = 0;
   
    protected:
     ServerStatusContext(bool);
   
     // If true print verbose output
     const bool verbose_;
   };
   
   //==============================================================================
   class InferContext {
    public:
     //==============
     class Input {
      public:
       virtual ~Input(){};
   
       virtual const std::string& Name() const = 0;
   
       virtual int64_t ByteSize() const = 0;
   
       virtual size_t TotalByteSize() const = 0;
   
       virtual DataType DType() const = 0;
   
       virtual ModelInput::Format Format() const = 0;
   
       virtual const DimsList& Dims() const = 0;
   
       virtual Error Reset() = 0;
   
       virtual const std::vector<int64_t>& Shape() const = 0;
   
       virtual Error SetShape(const std::vector<int64_t>& dims) = 0;
   
       virtual Error SetRaw(const uint8_t* input, size_t input_byte_size) = 0;
   
       virtual Error SetRaw(const std::vector<uint8_t>& input) = 0;
   
       virtual Error SetFromString(const std::vector<std::string>& input) = 0;
     };
   
     //==============
     class Output {
      public:
       virtual ~Output(){};
   
       virtual const std::string& Name() const = 0;
   
       virtual DataType DType() const = 0;
   
       virtual const DimsList& Dims() const = 0;
     };
   
     //==============
     class Result {
      public:
       virtual ~Result(){};
   
       enum ResultFormat {
         RAW = 0,
   
         CLASS = 1
       };
   
       virtual const std::string& ModelName() const = 0;
   
       virtual int64_t ModelVersion() const = 0;
   
       virtual const std::shared_ptr<Output> GetOutput() const = 0;
   
       virtual Error GetRawShape(std::vector<int64_t>* shape) const = 0;
   
       virtual Error GetRaw(
           size_t batch_idx, const std::vector<uint8_t>** buf) const = 0;
   
       virtual Error GetRawAtCursor(
           size_t batch_idx, const uint8_t** buf, size_t adv_byte_size) = 0;
   
       template <typename T>
       Error GetRawAtCursor(size_t batch_idx, T* out);
   
       struct ClassResult {
         size_t idx;
         float value;
         std::string label;
       };
   
       virtual Error GetClassCount(size_t batch_idx, size_t* cnt) const = 0;
   
       virtual Error GetClassAtCursor(size_t batch_idx, ClassResult* result) = 0;
   
       virtual Error ResetCursors() = 0;
   
       virtual Error ResetCursor(size_t batch_idx) = 0;
     };
   
     //==============
     class Options {
      public:
       virtual ~Options(){};
   
       static Error Create(std::unique_ptr<Options>* options);
   
       virtual bool Flag(InferRequestHeader::Flag flag) const = 0;
   
       virtual void SetFlag(InferRequestHeader::Flag flag, bool value) = 0;
   
       virtual uint32_t Flags() const = 0;
   
       virtual void SetFlags(uint32_t flags) = 0;
   
       virtual size_t BatchSize() const = 0;
   
       virtual void SetBatchSize(size_t batch_size) = 0;
   
       virtual Error AddRawResult(
           const std::shared_ptr<InferContext::Output>& output) = 0;
   
       virtual Error AddClassResult(
           const std::shared_ptr<InferContext::Output>& output, uint64_t k) = 0;
     };
   
     //==============
     class Request {
      public:
       virtual ~Request() = default;
   
       virtual uint64_t Id() const = 0;
     };
   
     //==============
     struct Stat {
       size_t completed_request_count;
   
       uint64_t cumulative_total_request_time_ns;
   
       uint64_t cumulative_send_time_ns;
   
       uint64_t cumulative_receive_time_ns;
   
       Stat()
           : completed_request_count(0), cumulative_total_request_time_ns(0),
             cumulative_send_time_ns(0), cumulative_receive_time_ns(0)
       {
       }
     };
   
     //==============
     class RequestTimers {
      public:
       enum Kind {
         REQUEST_START,
         REQUEST_END,
         SEND_START,
         SEND_END,
         RECEIVE_START,
         RECEIVE_END
       };
   
       RequestTimers();
   
       Error Reset();
   
       Error Record(Kind kind);
   
      private:
       friend class InferContext;
       friend class InferHttpContext;
       friend class InferGrpcContext;
       friend class InferGrpcStreamContext;
       struct timespec request_start_;
       struct timespec request_end_;
       struct timespec send_start_;
       struct timespec send_end_;
       struct timespec receive_start_;
       struct timespec receive_end_;
     };
   
    public:
     using ResultMap = std::map<std::string, std::unique_ptr<Result>>;
   
     virtual ~InferContext() = default;
   
     const std::string& ModelName() const { return model_name_; }
   
     int64_t ModelVersion() const { return model_version_; }
   
     uint64_t MaxBatchSize() const { return max_batch_size_; }
   
     const std::vector<std::shared_ptr<Input>>& Inputs() const { return inputs_; }
   
     const std::vector<std::shared_ptr<Output>>& Outputs() const
     {
       return outputs_;
     }
   
     Error GetInput(const std::string& name, std::shared_ptr<Input>* input) const;
   
     Error GetOutput(
         const std::string& name, std::shared_ptr<Output>* output) const;
   
     Error SetRunOptions(const Options& options);
   
     Error GetStat(Stat* stat);
   
     virtual Error Run(ResultMap* results) = 0;
   
     virtual Error AsyncRun(std::shared_ptr<Request>* async_request) = 0;
   
     virtual Error GetAsyncRunResults(
         ResultMap* results, const std::shared_ptr<Request>& async_request,
         bool wait) = 0;
   
     Error GetReadyAsyncRequest(
         std::shared_ptr<Request>* async_request, bool wait);
   
    protected:
     InferContext(const std::string&, int64_t, CorrelationID, bool);
   
     // Function for worker thread to proceed the data transfer for all requests
     virtual void AsyncTransfer() = 0;
   
     // Helper function called before inference to prepare 'request'
     virtual Error PreRunProcessing(std::shared_ptr<Request>& request) = 0;
   
     // Helper function called by GetAsyncRunResults() to check if the request
     // is ready. If the request is valid and wait == true,
     // the function will block until request is ready.
     Error IsRequestReady(
         const std::shared_ptr<Request>& async_request, bool wait);
   
     // Update the context stat with the given timer
     Error UpdateStat(const RequestTimers& timer);
   
     using AsyncReqMap = std::map<uintptr_t, std::shared_ptr<Request>>;
   
     // map to record ongoing asynchronous requests with pointer to easy handle
     // as key
     AsyncReqMap ongoing_async_requests_;
   
     // Model name
     const std::string model_name_;
   
     // Model version
     const int64_t model_version_;
   
     // The correlation ID to use with all inference requests using this
     // context. A value of 0 (zero) indicates no correlation ID.
     const CorrelationID correlation_id_;
   
     // If true print verbose output
     const bool verbose_;
   
     // Maximum batch size supported by this context. A maximum batch
     // size indicates that the context does not support batching and so
     // only a single inference at a time can be performed.
     uint64_t max_batch_size_;
   
     // Requested batch size for inference request
     uint64_t batch_size_;
   
     // Use to assign unique identifier for each asynchronous request
     uint64_t async_request_id_;
   
     // The inputs and outputs
     std::vector<std::shared_ptr<Input>> inputs_;
     std::vector<std::shared_ptr<Output>> outputs_;
   
     // Settings generated by current option
     // InferRequestHeader protobuf describing the request
     InferRequestHeader infer_request_;
   
     // Standalone request context used for synchronous request
     std::shared_ptr<Request> sync_request_;
   
     // The statistic of the current context
     Stat context_stat_;
   
     // worker thread that will perform the asynchronous transfer
     std::thread worker_;
   
     // Avoid race condition between main thread and worker thread
     std::mutex mutex_;
   
     // Condition variable used for waiting on asynchronous request
     std::condition_variable cv_;
   
     // signal for worker thread to stop
     bool exiting_;
   };
   
   //==============================================================================
   class ProfileContext {
    public:
     Error StartProfile();
   
     // \return Error object indicating success or failure.
     Error StopProfile();
   
    protected:
     ProfileContext(bool);
     virtual Error SendCommand(const std::string& cmd_str) = 0;
   
     // If true print verbose output
     const bool verbose_;
   };
   
   //==============================================================================
   class ServerHealthHttpContext : public ServerHealthContext {
    public:
     static Error Create(
         std::unique_ptr<ServerHealthContext>* ctx, const std::string& server_url,
         bool verbose = false);
   
     Error GetReady(bool* ready) override;
     Error GetLive(bool* live) override;
   
    private:
     ServerHealthHttpContext(const std::string&, bool);
     Error GetHealth(const std::string& url, bool* health);
   
     // URL for health endpoint on inference server.
     const std::string url_;
   };
   
   //==============================================================================
   class ServerStatusHttpContext : public ServerStatusContext {
    public:
     static Error Create(
         std::unique_ptr<ServerStatusContext>* ctx, const std::string& server_url,
         bool verbose = false);
   
     static Error Create(
         std::unique_ptr<ServerStatusContext>* ctx, const std::string& server_url,
         const std::string& model_name, bool verbose = false);
   
     Error GetServerStatus(ServerStatus* status) override;
   
    private:
     static size_t ResponseHeaderHandler(void*, size_t, size_t, void*);
     static size_t ResponseHandler(void*, size_t, size_t, void*);
   
     ServerStatusHttpContext(const std::string&, bool);
     ServerStatusHttpContext(const std::string&, const std::string&, bool);
   
     // URL for status endpoint on inference server.
     const std::string url_;
   
     // RequestStatus received in server response
     RequestStatus request_status_;
   
     // Serialized ServerStatus response from server.
     std::string response_;
   };
   
   //==============================================================================
   class InferHttpContext : public InferContext {
    public:
     ~InferHttpContext() override;
   
     static Error Create(
         std::unique_ptr<InferContext>* ctx, const std::string& server_url,
         const std::string& model_name, int64_t model_version = -1,
         bool verbose = false);
   
     static Error Create(
         std::unique_ptr<InferContext>* ctx, CorrelationID correlation_id,
         const std::string& server_url, const std::string& model_name,
         int64_t model_version = -1, bool verbose = false);
   
     Error Run(ResultMap* results) override;
     Error AsyncRun(std::shared_ptr<Request>* async_request) override;
     Error GetAsyncRunResults(
         ResultMap* results, const std::shared_ptr<Request>& async_request,
         bool wait) override;
   
    private:
     static size_t RequestProvider(void*, size_t, size_t, void*);
     static size_t ResponseHeaderHandler(void*, size_t, size_t, void*);
     static size_t ResponseHandler(void*, size_t, size_t, void*);
   
     InferHttpContext(
         const std::string&, const std::string&, int64_t, CorrelationID, bool);
   
     // @see InferContext.AsyncTransfer()
     void AsyncTransfer() override;
   
     // @see InferContext.PreRunProcessing()
     Error PreRunProcessing(std::shared_ptr<Request>& request) override;
   
     // curl multi handle for processing asynchronous requests
     CURLM* multi_handle_;
   
     // URL to POST to
     std::string url_;
   
     // Serialized InferRequestHeader
     std::string infer_request_str_;
   
     // Keep an easy handle alive to reuse the connection
     CURL* curl_;
   };
   
   //==============================================================================
   class ProfileHttpContext : public ProfileContext {
    public:
     static Error Create(
         std::unique_ptr<ProfileContext>* ctx, const std::string& server_url,
         bool verbose = false);
   
    private:
     static size_t ResponseHeaderHandler(void*, size_t, size_t, void*);
   
     ProfileHttpContext(const std::string&, bool);
     Error SendCommand(const std::string& cmd_str) override;
   
     // URL for status endpoint on inference server.
     const std::string url_;
   
     // RequestStatus received in server response
     RequestStatus request_status_;
   };
   
   //==============================================================================
   class ServerHealthGrpcContext : public ServerHealthContext {
    public:
     static Error Create(
         std::unique_ptr<ServerHealthContext>* ctx, const std::string& server_url,
         bool verbose = false);
   
     Error GetReady(bool* ready) override;
     Error GetLive(bool* live) override;
   
    private:
     ServerHealthGrpcContext(const std::string&, bool);
     Error GetHealth(const std::string& mode, bool* health);
   
     // GRPC end point.
     std::unique_ptr<GRPCService::Stub> stub_;
   };
   
   //==============================================================================
   class ServerStatusGrpcContext : public ServerStatusContext {
    public:
     static Error Create(
         std::unique_ptr<ServerStatusContext>* ctx, const std::string& server_url,
         bool verbose = false);
   
     static Error Create(
         std::unique_ptr<ServerStatusContext>* ctx, const std::string& server_url,
         const std::string& model_name, bool verbose = false);
   
     Error GetServerStatus(ServerStatus* status) override;
   
    private:
     ServerStatusGrpcContext(const std::string&, bool);
     ServerStatusGrpcContext(const std::string&, const std::string&, bool);
   
     // Model name
     const std::string model_name_;
   
     // GRPC end point.
     std::unique_ptr<GRPCService::Stub> stub_;
   };
   
   //==============================================================================
   class InferGrpcContext : public InferContext {
    public:
     virtual ~InferGrpcContext() override;
   
     static Error Create(
         std::unique_ptr<InferContext>* ctx, const std::string& server_url,
         const std::string& model_name, int64_t model_version = -1,
         bool verbose = false);
   
     static Error Create(
         std::unique_ptr<InferContext>* ctx, CorrelationID correlation_id,
         const std::string& server_url, const std::string& model_name,
         int64_t model_version = -1, bool verbose = false);
   
     virtual Error Run(ResultMap* results) override;
     virtual Error AsyncRun(std::shared_ptr<Request>* async_request) override;
     Error GetAsyncRunResults(
         ResultMap* results, const std::shared_ptr<Request>& async_request,
         bool wait) override;
   
    protected:
     InferGrpcContext(
         const std::string&, const std::string&, int64_t, CorrelationID, bool);
   
     // Helper function to initialize the context
     Error InitHelper(
         const std::string& server_url, const std::string& model_name,
         bool verbose);
   
     // @see InferContext.AsyncTransfer()
     virtual void AsyncTransfer() override;
   
     // @see InferContext.PreRunProcessing()
     Error PreRunProcessing(std::shared_ptr<Request>& request) override;
   
     // The producer-consumer queue used to communicate asynchronously with
     // the GRPC runtime.
     grpc::CompletionQueue async_request_completion_queue_;
   
     // GRPC end point.
     std::unique_ptr<GRPCService::Stub> stub_;
   
     // request for GRPC call, one request object can be used for multiple calls
     // since it can be overwritten as soon as the GRPC send finishes.
     InferRequest request_;
   };
   
   //==============================================================================
   class InferGrpcStreamContext : public InferGrpcContext {
    public:
     ~InferGrpcStreamContext() override;
   
     static Error Create(
         std::unique_ptr<InferContext>* ctx, const std::string& server_url,
         const std::string& model_name, int64_t model_version = -1,
         bool verbose = false);
   
     static Error Create(
         std::unique_ptr<InferContext>* ctx, CorrelationID correlation_id,
         const std::string& server_url, const std::string& model_name,
         int64_t model_version = -1, bool verbose = false);
   
     Error Run(ResultMap* results) override;
     Error AsyncRun(std::shared_ptr<Request>* async_request) override;
   
    private:
     InferGrpcStreamContext(
         const std::string&, const std::string&, int64_t, CorrelationID, bool);
   
     // @see InferContext.AsyncTransfer()
     void AsyncTransfer() override;
   
     // gRPC objects for using the streaming API
     grpc::ClientContext context_;
     std::shared_ptr<grpc::ClientReaderWriter<InferRequest, InferResponse>>
         stream_;
   };
   
   //==============================================================================
   class ProfileGrpcContext : public ProfileContext {
    public:
     static Error Create(
         std::unique_ptr<ProfileContext>* ctx, const std::string& server_url,
         bool verbose = false);
   
    private:
     ProfileGrpcContext(const std::string&, bool);
     Error SendCommand(const std::string& cmd_str) override;
   
     // GRPC end point.
     std::unique_ptr<GRPCService::Stub> stub_;
   };
   
   //==============================================================================
   
   std::ostream& operator<<(std::ostream&, const Error&);
   
   template <>
   Error InferContext::Result::GetRawAtCursor(size_t batch_idx, std::string* out);
   
   template <typename T>
   Error
   InferContext::Result::GetRawAtCursor(size_t batch_idx, T* out)
   {
     const uint8_t* buf;
     Error err = GetRawAtCursor(batch_idx, &buf, sizeof(T));
     if (!err.IsOk()) {
       return err;
     }
   
     std::copy(buf, buf + sizeof(T), reinterpret_cast<uint8_t*>(out));
     return Error::Success;
   }
   
   }}}  // namespace nvidia::inferenceserver::client
