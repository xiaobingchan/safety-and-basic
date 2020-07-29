package com.ruyou.web.base.project.util;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.ruyou.web.base.project.config.idcard.IdCardParam;
import org.apache.http.HttpResponse;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import static org.apache.commons.codec.binary.Base64.encodeBase64;

public class BusinessLicenseUtil {
    private static final Logger logger = LoggerFactory.getLogger(BusinessLicenseUtil.class);
    public static void main(String[] args) {
        String host = "https://dm-58.data.aliyun.com";
        String path = "/rest/160601/ocr/ocr_business_license.json";
        String method = "POST";
        String appcode = "59a87d08fee34f06b5fa319c72aaf84f";
        Map<String, String> headers = new HashMap<String, String>();
        //最后在header中的格式(中间是英文空格)为Authorization:APPCODE 83359fd73fe94948385f570e3c139105
        headers.put("Authorization", "APPCODE " + appcode);
        //根据API的要求，定义相对应的Content-Type
        headers.put("Content-Type", "application/json; charset=UTF-8");
        Map<String, String> querys = new HashMap<String, String>();
        String imgFile = "C:\\Users\\Administrator\\Desktop\\img\\timg.jpg";
        String imgBase64 = "";
        try {
            File file = new File(imgFile);
            byte[] content = new byte[(int) file.length()];
            FileInputStream finputstream = new FileInputStream(file);
            finputstream.read(content);
            finputstream.close();
            imgBase64 = new String(encodeBase64(content));
        } catch (IOException e) {
            e.printStackTrace();
        }
        //String bodys = "{\"image\":\"图片二进制数据的base64编码或者图片url\"}";
        String bodys = "{\"image\":\""+imgBase64+"\"}";
        try {
            /**
             * 重要提示如下:
             * HttpUtils请从
             * https://github.com/aliyun/api-gateway-demo-sign-java/blob/master/src/main/java/com/aliyun/api/gateway/demo/util/HttpUtils.java
             * 下载
             *
             * 相应的依赖请参照
             * https://github.com/aliyun/api-gateway-demo-sign-java/blob/master/pom.xml
             */
            HttpResponse response = HttpUtils.doPost(host, path, method, headers, querys, bodys);
            //System.out.println(response.toString());
            //获取response的body
            logger.info(EntityUtils.toString(response.getEntity()));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static JSONObject getBusinessLicenseMessage(String imgBase64){
        IdCardParam idCardParam = SpringContextUtil.getBean("idCardParam");
        String host = "https://dm-58.data.aliyun.com";
        String path = "/rest/160601/ocr/ocr_business_license.json";
        String method = "POST";
        String appcode = idCardParam.getLicenseAppcode();
        Map<String, String> headers = new HashMap<String, String>();
        //最后在header中的格式(中间是英文空格)为Authorization:APPCODE 83359fd73fe94948385f570e3c139105
        headers.put("Authorization", "APPCODE " + appcode);
        //根据API的要求，定义相对应的Content-Type
        headers.put("Content-Type", "application/json; charset=UTF-8");
        Map<String, String> querys = new HashMap<String, String>();
        String imgFile = "C:\\Users\\Administrator\\Desktop\\img\\timg.jpg";
        /*String imgBase64 = "";
        try {
            File file = new File(imgFile);
            byte[] content = new byte[(int) file.length()];
            FileInputStream finputstream = new FileInputStream(file);
            finputstream.read(content);
            finputstream.close();
            imgBase64 = new String(encodeBase64(content));
        } catch (IOException e) {
            e.printStackTrace();
        }*/
        //String bodys = "{\"image\":\"图片二进制数据的base64编码或者图片url\"}";
        String bodys = "{\"image\":\""+imgBase64+"\"}";
        JSONObject jsonObject = null;
        try {
            /**
             * 重要提示如下:
             * HttpUtils请从
             * https://github.com/aliyun/api-gateway-demo-sign-java/blob/master/src/main/java/com/aliyun/api/gateway/demo/util/HttpUtils.java
             * 下载
             *
             * 相应的依赖请参照
             * https://github.com/aliyun/api-gateway-demo-sign-java/blob/master/pom.xml
             */
            HttpResponse response = HttpUtils.doPost(host, path, method, headers, querys, bodys);
            int stat = response.getStatusLine().getStatusCode();
            if(stat != 200){
                logger.info("Http code: " + stat);
                logger.info("http header error msg: "+ response.getFirstHeader("X-Ca-Error-Message"));
                logger.info("Http body error msg:" + EntityUtils.toString(response.getEntity()));
            } else {
                //如果上面的stat的状态不是200的话，那么上面一行中的System.out.println("Http body error msg:" + EntityUtils.toString(response.getEntity()));
                //会把response.getEntity()的使用次数用完，只有一次使用这个方法的机会
                String res = EntityUtils.toString(response.getEntity());
                jsonObject = JSON.parseObject(res);
            }
            //System.out.println(response.toString());
            //获取response的body
            //EntityUtils.toString(response.getEntity());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return jsonObject;
    }

}
