#!/usr/bin/python

import os
import random
import time
import traceback
from concurrent import futures

import grpc
import demo_pb2
import demo_pb2_grpc

from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')


class AdServiceV2():
    # TODO:
    # Implemet the Ad service business logic

    # Uncomment to enable the HealthChecks for the Ad service
    # Note: These are needed for the liveness and readiness probes
     def Check(self, request, context):
         return health_pb2.HealthCheckResponse(
             status=health_pb2.HealthCheckResponse.SERVING)
    
     def Watch(self, request, context):
         return health_pb2.HealthCheckResponse(
             status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)

     def GetRandomProductId(self):
         channel = grpc.insecure_channel("localhost:3550")
         stub = demo_pb2_grpc.ProductCatalogServiceStub(channel)
         request  = demo_pb2.Empty()
         response = stub.ListProducts(request)
         product_id = random.choice(response.products).id
         return product_id


if __name__ == "__main__":
    logger.info("initializing adservice-v2")

    # TODO:
    # create gRPC server, add the Ad-v2 service and start it

    # Uncomment to add the HealthChecks to the gRPC server to the Ad-v2 service
    health_pb2_grpc.add_HealthServicer_to_server(AdServicer(), server)

    class AdServicer(demo_pb2_grpc.AdServiceV2Servicer):

        def GetAds(self, request, context):
            id = AdServiceV2.GetRandomProductId

            product_info = {
                "id" : id,
                "text" : "AdV2 - Items with 25% discount!"
            }
            return demo_pb2.AdResponse(product_info)

    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    demo_pb2_grpc.add_AdServiceV2Servicer_to_server(AdServicer(), server)


    print("Server starting on port 9556...")
    server.add_insecure_port("[::]:9556")
    server.start()
    # Keep thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)