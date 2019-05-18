# rokid_webhook

 _Rokid (若琪) webhook home assistant component._ 

 在home assistant中使用服务调用若琪webhook实现tts播报, 播放音乐流媒体文件, 执行asr指令。

## 安装 & 配置

 1. 将 `rokid_webhook` 目录保存到 `config/custom_components/`
 2. 在 `configuration.yaml` 中添加 
    ```
    rokid_webhook:  
      webhook_id: 'YOUR WEBHOOK ID'  
    ```
    
    可选参数：    
    ```
      sn:   
      roomName:  
      tag:  
      isAll: False  
    ```
 3. 重启 home assistant

## 使用
 1. 在界面上使用服务工具调试
 2. 在自动化或者脚本里面调用
 
```
service: rokid_webhook.tts
data:
  message: 'hello 主人'

service: rokid_webhook.audio
data:
  message: 'http://HASSIO_IP:8123/local/audio.mp3'

service: rokid_webhook.asr
data:
  message: '明天天气怎么样'
```

## 参考
  [官方文档](https://developer.rokid.com/docs/rokid-homebase-docs/webhook/)



