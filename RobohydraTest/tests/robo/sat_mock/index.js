var RoboHydraHeadStatic = require("robohydra").heads.RoboHydraHeadStatic;
var RoboHydraHead = require("robohydra").heads.RoboHydraHead;

var log4js = require('log4js');
var log4js_config = {
    "appenders": [{
        "type": "console",
        "layout": {
            "type": "pattern",
            "pattern": "%[%d{ISO8601_WITH_TZ_OFFSET} %p %c -%] %m",
            "tokens": {}
        }
    }]
};

log4js.configure(log4js_config, {});
var fc = log4js.getLogger('SERVER::sat_MOCK');



exports.getBodyParts = function(conf) {
    return {
        heads: [new RoboHydraHead({
            path:'/requestlist',
            handler:function(req,res){
            	fc.info('/requestlist - handler head');
                res.statusCode=200;
                res.send(JSON.stringify("{sat:10}"));
                fc.info('/requestlist - handler');
            }
        }),
        new RoboHydraHead({
            path:'/sat',
            handler:function(req,res){
            	fc.info('/sat -call');
            	if (req.method === 'POST'){
            		res.statusCode=200;
                    res.send(JSON.stringify("{sat:20}"));           		
                    }
            }
         })
        ]
    };
};