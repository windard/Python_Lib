## schematics

有一个数据格式化库，主要就是为了数据格式化，转化成可以解析引用指定格式的数据。

其实和上一个数据序列化库 marshmallow 有点像，都是数据格式转化的，但是这个没有那个好用，但是那个也有其他的问题, 比如兼容性问题。

schematic 的数据 Model 中主要有两种类型，`primitive_type` 和 `native_type`, 一种是 基准类型 一种是原生类型，基准类型指的是 int，str，bool 等 json 格式可以解析的数据类型，原生类型就是 python 语言中包含的类型，比如 datetime.datetime, uuid.UUID 等。

可能这个库唯一比 marshmallow 优秀的一点是在于它可以生成 Model，而 marshmallow 序列化和反序列化的结果都是 dict

> Model 的实例化时还有一个参数 `strict` 需要注意一下，默认对于不识别的参数会报错，😂

```python
# -*- coding: utf-8 -*-

import datetime
from schematics import Model
from schematics.types import IntType, StringType, ListType, DateTimeType


class BigIntType(IntType):
    # primitive_type = str
    # native_type = str

    def to_native(self, value, context=None):
        # 转成 python 数据格式，比如 Datetime 或者 Decimal
        return super(BigIntType, self).to_native(value, context)

    def to_primitive(self, value, context=None):
        # 转成原生数据格式，更易于使用 json 序列化
        return str(value)


class SetType(ListType):
    primitive_type = set
    native_type = set

    def to_native(self, value, context=None):
        pass


class UTCDatetimeTime(DateTimeType):
    primitive_type = str
    native_type = datetime.datetime

    def to_native(self, value, context=None):
        pass

    def to_primitive(self, value, context=None):
        pass


class Plugin(Model):
    app_id_list = ListType(BigIntType)
    app_name = StringType()


if __name__ == '__main__':
    plugin = Plugin({"app_id_list": ["1234", 2245345, "1324"], "app_name": "哈哈哈"})
    print(plugin.serialize())
    print(plugin.to_primitive())
    print(plugin.to_native())

```

