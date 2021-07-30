- 初始化

  ```python
  from zjvis import SummaryWriter
  summarywriter = SummaryWriter(log_dir: str='logs/',
                                max_queue: int = 10,
                                flush_secs: int = 120,
                                filename_suffix:str = '')
      """
          创建一个日志写入器，添加event
      Args:
          log_dir: 字符串，event文件写入的目录
          max_queue: 整数，文件每次flush前可追加event的队列大小，默认为10
          flush_secs: 整数，写入文件的时间间隔，默认为120s
          filename_suffix: 字符串，event文件的后缀
      """
  ```

- 模型结构

  可视化主流深度学习框架的网络模型，如**tensorflow**，**pytorch**,  **oneflow**等。

  1.主流神经网络模型

  ```python
  summarywriter.add_graph(model,
                          input_to_model: Union[tuple]=None,
                          model_type: str ='pytorch',
                          verbose: bool =False)
      """
          添加神经网络的图结构到日志，支持tensorflow，pytorch
      Args:
          model: 神经网络模型, torch.nn.Module、 tf.Session().graph， oneflow模型请通过onnx或者json格式导出
          input_to_model: 元组, 一组用于模型测试的输入
          model_type: 字符串，模型的类型为‘pytorch’ 或 'tensorflow'
          verbose: 布尔值，pytorch模型是否输出到控制台
      """
  ```

  2.onnx网络模型

  ```python
  summarywriter.add_onnx_graph(onnx_model_file：str):
      """
          添加onnx模型到日志
      Args:
          onnx_model_file: 字符串，onnx模型对应的文件路径
      """
  ```

  3.json网络模型 （oneflow）

  ```python
  summarywriter.add_json_graph(model_str: str,
                               name: str = 'model'):
      """
          该功能需要神经网络框架的支持，首先使用内部函数对网络模型的结构进行序列化，然后将序列化的字符串写入到json文件
      Args:
          model_str: 字符串，模型的序列化字符串
          name: 字符串，json文件名
      """
  ```

- 标量数据

  可视化标量数据随时间的变化趋势

  1.单个标量数据

  ```python
  summarywriter.add_scalar(tag: str,
                           scalar_value: Union[float, numpy_compatible],
                           step: Optional[int] = None):
      """
          添加单个标量数据到日志
      Args:
          tag: 字符串，数据标识
          scalar_value: 浮点数，标量的值
          step: 整数，可选参数，记录数据的step
      """
  ```

  2.多个标量数据

  ```python
  summarywriter.add_scalars(tag_scalar_dict: Dict[str, Union[float, numpy_compatible]],
                            step: Optional[int] = None):
      """
          添加一组标量数据到日志
      Args:
          tag_scalar_dict: 字典，(标签, 标量值)
          step: 整数，可选参数，记录数据的step
      """
  ```

- 媒体数据

  可视化神经网络中的样本数据，如图片，音频，视频，文本等。

  **图像**

  1.单张图片

  ```python
  summarywriter.add_image(tag: str,
                          tensor: numpy_compatible,
                          step: Optional[int] = None):
      """
          添加单张图像数据到日志
      Args:
          tag: 字符串，图像的标识
          tensor: 数组，图像数据，'uint8' 或 'float' 类型的数据，大小为(H,W) 或 (H,W,C), 其中C为1,2,3,4
          step: 整数，可选参数，记录数据的step
      """
  ```

  2.多张图片

  ```python
  summarywriter.add_images(tag: str,
                           tensors: numpy_compatible,
                           step: Optional[int] = None):
      """
          添加多个图像数据到日志
      Args:
          tag: 字符串, 图像的标识, 导出过程中将自动转化为tag_1, tag_2, ... , tag_k
          tensors: 数组类型，图像数据，'uint8' 或 'float' 类型的数据，大小为(K,H,W) 或 (K,H,W,C), 其中C为1,3,4
          step: 可选参数，记录数据的step
      """
  ```

  **文本**

  ```python
  summarywriter.add_text(tag: str,
                         text_string: str,
                         step: Optional[int] = None):
      """
          添加文本数据到日志
      Args:
          tag: 字符串，文本的标识
          text_string: 字符串，文本字符串
          step: 整数，可选参数，记录数据的step
      """
  ```

  **音频**

  ```python
  summarywriter.add_audio(tag: str,
                          audio_tensor: numpy_compatible,
                          step: Optional[int],
                          sample_rate: Optional[int] = 44100):
      """
          添加音频数据到日志
      Args:
          tag: 字符串，音频的标识
          audio_tensor: 数组，音频数据，大小为(L, C), 其中L为音频帧的长度，C为通道，通常C=1，2
          step: 整数，可选参数，记录数据的step
          sample_rate: 整数，采样率 Hz
      """
  ```

  **视频**

  ```python
  summarywriter.add_video(tag: str,
                          video_tensor: numpy_compatible,
                          step: Optional[int] = None,
                          fps: Optional[Union[int, float]] = 4):
      """
          添加视频数据到日志
      Args:
          tag: 字符串，视频的标识
          video_tensor: 数组，视频数据
          step: 整数，可选参数，记录数据的step
          fps: 整数，可选参数，视频的帧率， 默认为4
      """
  ```

- 统计分析数据

  可视化数据的分布情况，如直方图，分布图。其中分布图由直方图转化得到

  ```python
  summarywriter.add_histogram(tag: str,
                              tensor: numpy_compatible,
                              step: Optional[int] = None,
                              max_bins: Optional[int] = None):
      """
          添加直方图数据到日志
      Args:
          tag: 字符串，直方图的标识
          tensor: 数组，直方图的原始数据
          step: 整数，可选参数，记录数据的step
          max_bins: 整数，可选参数，直方图划分的区间个数
      """
  ```

- 降维分析数据

  可视化高维数据的聚类。以动画的形式显示样本数据在各网络层中产生的高维嵌入的聚类变化

  1.可视化的样本数据，只需在训练的开始或结束添加一次即可，tag应与产生的高维嵌入数据的tag保持一致

  ```python
  summarywriter.add_embedding_sample(tag: str,
                                     tensor: numpy_compatible,
                                     sample_type: str):
      """
          添加降维处理的高维数据对应的样本到日志，以便查看降维后数据点对应的原始样本
      Args:
          tag: 字符串，高维数据样本的标识，应与高维数据保持一致
          tensor: 数组，高维数据的样本，数据类型，大小为[N,*]
          sample_type: 字符串，样本数据的类型，支持‘image’,'text','audio'
      """
  ```

  2.样本数据产生的高维嵌入数据

  ```python
  summarywriter.add_embedding(tag: str,
                              tensor: numpy_compatible,
                              label: Optional[numpy_compatible] =None,
                              step: Optional[int] = None):
      """
          添加降维处理的高维数据到日志
      Args:
          tag: 字符串，降维处理的高维数据的标识，应与高维数据的样本标识相同
          tensor: 数组，高维数据的样本，大小为[N,*]
          label: 数组，可选参数，高维数据对应的类别标签，大小为[N]
          step: 整数，可选参数，记录数据的step
      """
  ```
  <br>
  **ps**:可视化高维数据提供了两种方式：

  （a）使用**同一组测试数据**在不同step生成高维嵌入数据。用户通过add_embedding_sample添加测试的样本数据，在可视化过程中可通过点击样本点查看原始样本。
    ```python
        model = MinistNet()
        test_x, test_y = dataset()
        
        writer.add_embedding_sample(tag='test', tensor=test_x, sample_type='iamge')   
        
        for step in range(steps):
            # 1.train stage
            model.train()
                 .....
            
            # 2.eval stage
            model.eval()
            out = model.forward(test_x)
            writer.add_embedding(tag='test', tensor=out, label=test_y, step=step)
    ```
    
  （b）使用**不同的数据**在不同的step生成高维嵌入数据。 此时每个step的样本数据并不相同，不再支持查看降维后每个样本点对应的样本数据。用户无需通过add_embedding_sample添加样本数据，否则查看的样本点数据将出现不一致等问题。
    ```python
        model = MinistNet()
        train_x, train_y = dataset()
        for step in range(steps):
            # 1.train stage
            model.train()
            out = model.forward(train_x)
            writer.add_embedding(tag='train', tensor=out, label=train_y, step=step)
    ```
- 异常检测数据

  可视化各网络层的权重，偏置，梯度，输出的异常情况。主要以直方图，箱线图，颜色映射矩阵等方式进行展示

  ```python
  summarywriter.add_exception(tag: str,
                              tensor: numpy_compatible,
                              step: Optional[int] = None):
      """
          添加监测的异常数据到日志
      Args:
          tag: 字符串，待监测的异常数据的标识
          tensor: 数组，待监测的异常数据
          step: 整数，可选参数，记录数据的step
      """
  ```

- 超参数

  可视化同一个或多个网络模型在不同超参数组合的训练结果

  ```python
  summarywriter.add_hparams(hparam_dict: Dict[str, Union[bool, str, float, int]],
                            metrics: Optional[Union[list, tuple]] =None,
                            tag: Optional[str] = None):
      """
          添加一组数据到日志
      Args:
          hparam_dict: 字典，模型的超参数
          metrics: 列表、元组，可选参数， 需要记录的度量指标，该指标必须在scalar中已定义
          tag: 字符串，可选参数，超参数的标识
      """
  ```

  