# rokid_webhook

 _Rokid (若琪) webhook home assistant component._ 

 在home assistant中使用服务调用若琪webhook实现tts播报, 播放音乐流媒体文件, 执行asr指令。

## 安装 
* 将 `rokid_webhook` 目录保存到 `config/custom_components/`

* 支持 `custome_updater` 
```
custom_updater:
  track:
    - cards
    - components
  component_urls:
    - https://raw.githubusercontent.com/jihao/rokid-webhook-hass/master/rokid_webhook.json
```

## 配置

 1. 在 `configuration.yaml` 中添加 
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
 2. 重启 home assistant

## 使用
 1. 在界面上使用服务工具调试 
 2. 在自动化或者脚本里面调用
 
* rokid_webhook.tts
 
```diff
+ 服务调用时如果指定可选参数，将覆盖configuration.yaml里的默认配置。

 Example: {"message":"Hello 主人", "webhook_id":"your_overwrite_id", "sn":"device_sn", "roomName":"客厅"}
```


| 参数          | 类型           | 描述   |示例 |
| ------------- | ------------- | ------------- | ------------- |
| message       | 必选          |   播报内容	    | Hello 主人     |
| webhook_id    | 可选          | Webhook地址的标识	| your_very_unique_token|
| sn            | 可选          | 若琪序列号	     |device_sn      |
| roomName      | 可选          | 若琪所处的房间	 | 客厅           |
| tag           | 可选          | 设备标签	      |TAG_A           |
| isAll         | 可选          | 选择所有设备，默认 false	 | true |

* rokid_webhook.audio

| 参数          | 类型           | 描述   |示例 |
| ------------- | ------------- | ------------- | ------------- |
| message       | 必选          |   音频地址	    | http://HASSIO_IP:8123/local/audio.mp3     |
| 所有可选参数同上  |

* rokid_webhook.asr

| 参数          | 类型           | 描述   |示例 |
| ------------- | ------------- | ------------- | ------------- |
| message       | 必选          |   语音控制指令	    | 今天天气怎么样     |
| 所有可选参数同上  |


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



