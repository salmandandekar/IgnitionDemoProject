
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
class ModelOpsService(object):
    @traced()
    def log_inference(self, model_id, inputs, outputs):
        router.publish("ai.inference.logged", make("log","aiInference",{"model":model_id,"inputs":inputs,"outputs":outputs}))
        return True
