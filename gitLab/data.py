#-*- coding: utf-8 -*-

import os, sys, json, re, base64
file_path = os.path.dirname( os.path.abspath(__file__) ) + "/../"
sys.path.append( file_path )

from business.decorator import action
from util.data import dh
from business.custom_http import crypt_data
from util import phpserialize_impv as pimpv
from phpserialize import unserialize, loads, phpobject

class CustomData(object):
    
    @action
    def  get_regex_data( self, step, utdata ):
        
        flag, params = dh.param_rebuild( step.execute.params,  utdata.vars )
        if not flag:
            return None, "解析参数过程失败"
        
        flag, paths = dh.check_key_in_map( params, "text", "regex")
        if not flag:
            return None, "缺失必要参数: %s" % json.dumps( paths )
        
        text = params.get("text", "")
        regex = params.get("regex", "")
        dotall = params.get( "dotall", True )
        result = ""
        if dotall:
            result = re.findall( regex, text, re.DOTALL )
        else:
            result = re.findall( regex, text )
        if result == None:
            return False, "没有匹配到信息"
        else:
            return True, result

     @action   
     def  get_substr_data(self, step, utdata):
         flag, params = dh.param_rebuild(step.execute.params, utdata.vars)
         if not flag:
             return None, "解析参数过程失败"

         flag, paths = dh.check_key_in_map(params, "text", "regex")
         if not flag:
             return None, "缺失必要参数: %s" % json.dumps(paths)
         str= params.get("str","")
         regex=params.get("regex","")
         result=str[regex]
         if result == None:
             return False,"截取字符错误！"
         else:
             return True,result

    @action
    def  addVar( self, step, utdata ):
        
        flag, params = dh.param_rebuild( step.execute.params, utdata.vars )
        if not flag:
            return None, "解析参数过程失败"
        result = params.get("variable")
        if params.get("type") == True:
            try: result = eval( params.get("variable") )
            except: pass
        return True, result
    
    @action
    def  key_center_hndl( self, step, utdata ):
        
        flag, params = dh.param_rebuild( step.execute.params, utdata.vars )
        if not flag:
            return None , "解析参数过程失败"
        
        ntype = params.get("type")
        if ntype not in ["encrypt", "decrypt"]:
            return None, "解析参数类型只支持encrypt/decrypt"
        
        return crypt_data( data=params.get("data"), ctype=ntype )
    
    @action
    def  rebuild_b64_data( self, step, utdata ):
        
        flag, params = dh.param_rebuild(step.execute.params, utdata.vars)
        if not flag: 
            return  None, "解析参数过程失败"
        
        data = params.get("data")
        ttype = params.get("type")
        try:
            if ttype == "decode":
                return True, base64.b64decode( data )
            elif ttype == "encode":
                return True, base64.b64encode( data )
            else:
                return False, "不支持的操作类型"
        except:
            return None, "操作过程出现异常"
        
    @action
    def  json_marshal( self, step, utdata ):
        
        flag, params = dh.param_rebuild( step.execute.params, utdata.vars )
        if not flag:
            return None, "解析参数过程失败"
        
        data = params.get("data")
        ttype = params.get("type")
        if ttype not in ["marshal", "unmarshal"]:
            return None, "支持的type字段值为marshal/unmarshal"
        
        if data == "marshal":
            try: return  True, json.dumps( data )
            except: return False, "无法json序列化操作, data: %s" % data
        else:
            try: return True, json.loads( data )
            except: return False, "无法解序列化操作, data: %s" % data
                
    
    @action
    def  php_unmarshal( self, step, utdata ):

        flag, params = dh.param_rebuild( step.execute.params, utdata.vars )
        if not flag:
            return None, "解析参数过程失败"
        
        data = params.get("data")
        try:
            data = unserialize( data )
        except ValueError:
            try: data = loads( data, object_hook=phpobject )
            except: data = pimpv.loads( data.replace("O:8\"stdClass\"", "a"), object_hook=phpobject )
        except:
            return False, "提供的数据无法使用php方式解序列化"
        
        return True, data
        
    @action
    def   parse_to( self, step, utdata ):
        
        flag, params = dh.param_rebuild( step.execute.params, utdata.vars )
        if not flag: 
            return None, "解析参数过程失败"
        
        data = params.get( "data" )
        to = params.get( "to" )    
        if to not in ["string",  "float", "int", "dict", "map"]:
            return False, "当前只支持string/float/int格式的转换"
        
        try:
            if to=="string":
                return True, str(data)
            elif to == "float":
                return True, float( data )
            elif to == "int":
                return True, int( data )
            else:
                return True, eval( data )
        except:
            return False, "数据转换失败, data: %s, to: %s" % ( data, to )
        
    @action
    def  trim( self, step, utdata ):
        
        flag, params = dh.param_rebuild( step.execute.params, utdata.vars )
        if not flag:  return None, "解析参数过程失败"
        
        data = params.get("data")
        if not isinstance(data, str): return None, "参数类型错误"
        
        try: return True, data.strip()
        except: return False, "调用trim方法失败"
    
    @action
    def  createUUid(self, step, utdata):
        
        import  uuid
        nuuid = "xmguest-" + str(uuid.uuid1())
        return True, nuuid.upper()
        
    
        
        
        
