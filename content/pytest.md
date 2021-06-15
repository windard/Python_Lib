# pytest
pytest 作为 Python 中最著名的单元测试框架，一举超过 unittest，nose 等传统测试工具，因为其灵活便捷的使用方式，和功能强大的测试组件。

## 安装

```
pip install pytest
```

### 开始

```python
# -*- coding: utf-8 -*-


def test_equal():
    assert [1, 2, 3] == [1, 2, 3]


def test_not_equal():
    assert [1, 2, 3] != [3, 2, 1]
```

使用 pytest 运行即可

```
$ pytest -v test_equal.py
================================================================================================ test session starts =================================================================================================
platform darwin -- Python 3.7.6, pytest-5.4.1, py-1.8.1, pluggy-0.13.1 -- /Users/bytedance/miniconda/envs/api_auth/bin/python
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/Users/bytedance/repos/toutiao/app_3/pytest_demo/.hypothesis/examples')
rootdir: /Users/bytedance/repos/toutiao/app_3/pytest_demo
plugins: schemathesis-1.1.0, cov-2.12.0, subtests-0.2.1, ordering-0.6, hypothesis-5.49.0
collected 2 items

test_equal.py::test_equal PASSED                                                                                                                                                                               [ 50%]
test_equal.py::test_not_equal PASSED                                                                                                                                                                           [100%]

================================================================================================= 2 passed in 0.01s ==================================================================================================
```

1. 测试断言使用 Python 关键字 `asset` 。 
2. 使用 pytest 运行单测，使用 `-v` 参数获得详细输出
3. 测试文件一般由 `test_` 开头或者 `_test` 结尾，测试方法一般由 `test_` 开头，测试类一般由 `Test` 开头

### 捕获异常

```python
# -*- coding: utf-8 -*-

import pytest


def test_raise():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def divide(a, b):
    if b == 0:
        raise ValueError("Zero can't be used as a divisor")
    return a / b


def test_catch():
    with pytest.raises(ValueError) as e:
        divide(1, 0)

    assert e
    assert e.value.args[0] == "Zero can't be used as a divisor"
```

1. 使用 `pytest.raises` 上下文管理器捕获异常
2. 使用 `e.value` 可以获取原始异常，用来判断错误码或错误信息

### 参数化

```python
# -*- coding: utf-8 -*-

import pytest
import hashlib


@pytest.mark.parametrize(
    'user, password, landed',
    [
        ('jack', 'abcdefgh', True),
        ('admin', '88888888', False),
        ('tom', 'a123456a', True),
        ('root', 'root-password', False),
        ('mary', '1234567e', False),
        ('alice', '1234abcd', False),
    ],
)
def test_login(user, password, landed):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503',
        'root': 'a0e166c1accbb0f6fb4bbdd27f5b0ef7',
    }

    assert hashlib.md5(password.encode()).hexdigest() == db.get(user) or not landed
```

1. 使用 `pytest.mark.parametrize` 标记作为参数化传入
2. Pytest 还有很多其他功能强大的标记装饰器，比如跳过测试 `pytest.mark.skip`

## 进阶

### 固件(fixture)

固件是一些可以复用的通用函数，比如 生成数据，mock请求，打开连接，清理数据等。
> 也有翻译作 夹具

### 生成数据

```python
# -*- coding: utf-8 -*-

import pytest


@pytest.fixture()
def user_info():
    return {"name": "test user", "id": 10001}


def test_login(user_info):
    assert user_info['id'] == 10001


def test_register(user_info):
    assert user_info['name'] == "test user"
```

1. 生成静态数据，可以作为统一数据集中管理
2. Fixture 作为参数传入已经被自动执行，拿到的就是参数执行结果，无需再次调用。

```python
# -*- coding: utf-8 -*-

import pytest


@pytest.fixture()
def user_info_generator():
    user_id = 10000

    def _create(user_name):
        nonlocal user_id
        user_id += 1
        return {'name': user_name, 'id': user_id}

    return _create


def test_register(user_info_generator):
    user_name = "Peter"
    user_info = user_info_generator(user_name)
    assert user_info['id'] == 10001
    assert user_info['name'] == user_name

    user_name = "Lily"
    user_info = user_info_generator(user_name)
    assert user_info['id'] == 10002
    assert user_info['name'] == user_name
```

1. 生成动态数据，可以根据传入参数规则生成

### mock请求
在单元测试中一般不会依赖外部的网络，存储等基础设施，需要我们提前将外部依赖 mock 。

```python
# -*- coding: utf-8 -*-

import pytest
import requests


def test_requests(monkeypatch):
    def _get(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        return response

    monkeypatch.setattr(requests, 'get', _get)
    resp = requests.get("https://aasasxa.csdowecfer.cwebqascs")
    assert resp
    assert resp.status_code == 200


@pytest.fixture()
def mock_request_get(monkeypatch):
    def _get(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        return response

    monkeypatch.setattr(requests, 'get', _get)


def test_get_url(mock_request_get):
    resp = requests.get("https://ascf.qwefreas.com")
    assert resp
    assert resp.status_code == 200


@pytest.mark.usefixtures('mock_request_get')
def test_get():
    resp = requests.get("https://scdvqw.csdcdff.cascvr")
    assert resp
    assert resp.status_code == 200


@pytest.fixture()
def mock_request(monkeypatch):
    def _request(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        return response

    monkeypatch.setattr(requests, 'request', _request)


@pytest.mark.parametrize(
    'method, url',
    [
        ("GET", "https://ascdfvd.cdsfvsd.csdcdv"),
        ("GET", "https://cerfwreq.cev.cwec"),
        ("POST", "https://cdebsbce.cwev.cewvre"),
        ("PUT", "https://vsrgtbev.cer.cewvrev"),
    ],
)
@pytest.mark.usefixtures('mock_request')
def test_urls(method, url):
    resp = requests.request(method, url)
    assert resp
    assert resp.status_code == 200
```

1. Fixture 可以作为函数参数表示引用，也可以使用 `pytest.mark.usefixtures` 作为引用
2. 在一个 fixture 中可以引用另一个 fixture，可以嵌套使用
3. Pytest 中有很多内置 fixture，比如 `monkeypatch` 可以用来动态的修改类和模块，`tmpdir` 可以用来生成临时目录等，还可以使用第三方插件。
4. `monkeypatch` 常用的功能有动态的增删属性，增删元素，增删环境变量。
5. 可以使用 `pytest --fixtures` 查看所有的固件, 包括内置固件，自定义固件和第三方固件。

```python
# -*- coding: utf-8 -*-

import mock
import os


def test_os_isdir(monkeypatch):
    monkeypatch.setattr(os.path, 'isdir', mock.Mock(return_value=True))
    assert os.path.isdir("dcv/cdfacv/scdcs")


@mock.patch('os.path.isfile', mock.Mock(return_value=True))
def test_os_isfile():
    assert os.path.isfile("/adff/assassdf/a")
```

1. 如果是比较简单的 mock，也可以直接使用 `mock` 库来 patch
2. `mock.Mock` 可以用来表示任意对象，`return_value` 表示其作为函数执行时的返回值。
3. `mock` 可以和测试样例结合使用，但是不能在固件中使用，在固件中只能使用 monkeypatch
4. 或者使用 `pytest-mock` 库，可以提供 `monker` 固件，和 `mock` 的使用一致。

### 测试前后

```python
# -*- coding: utf-8 -*-

import pytest

data = []


@pytest.fixture
def clear_data():
    while data:
        data.pop()

    yield
    while data:
        data.pop()


@pytest.mark.usefixtures('clear_data')
def test_append():
    data.append(1)
    assert data
    assert len(data) == 1
    assert data[0] == 1


@pytest.mark.usefixtures('clear_data')
def test_pop():
    data.append(1)
    data.append(2)
    data.append(3)
    assert len(data) == 3
    assert data.pop() == 3
    assert len(data) == 2
    assert data.pop() == 2


@pytest.mark.usefixtures('clear_data')
def test_length():
    assert len(data) == 0
```

1. 固件的生命周期不止在测试前，也可以通过 `yield` 关键字，在测试后进行一些操作。

### 自动执行

```python
# -*- coding: utf-8 -*-

import time
import pytest

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


@pytest.fixture(autouse=True)
def timer_function_scope():
    start = time.time()
    yield
    print('\nTime cost: {:.3f}s'.format(time.time() - start))


@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\nTotal start: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    yield

    finished = time.time()
    print('Total finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total cost: {:.3f}s'.format(finished - start))


def test_assert_one():
    time.sleep(1)


def test_assert_two():
    time.sleep(2)
```

1. 在 pytest 中使用 `-s` 参数来获取屏幕输出，否则打印数据会被捕获拦截。
2. 对于一些通用必选的固件，可以使用 `autouse` 来自动执行，效果类似于 `setup` 和 `teardown`。
3. 固件的作用域默认是 `function` ，即在每个测试函数级别执行，也可以选择 `class`,`module`,`session` 等不同级别。
4. 同一级别的自动执行固件可以有多个，可以通过 `--setup-show` 查看自动执行的顺序。
5. 自定义的固件，一般会统一放在 `conftest.py` 中，pytest 会自动查找根目录下的 `conftest.py` 读取自定义的固件，而放在 `__init__.py` 不会被识别。
6. 在 pytest 中也支持 unittest 的写法，可以使用 `setup_function` 和 `teardown_function` 来做自动执行。

```
$ pytest -sv test_timer.py
================================================================================================ test session starts =================================================================================================
platform darwin -- Python 3.7.6, pytest-5.4.1, py-1.8.1, pluggy-0.13.1 -- /Users/bytedance/miniconda/envs/api_auth/bin/python
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/Users/bytedance/repos/toutiao/app_3/pytest_demo/.hypothesis/examples')
rootdir: /Users/bytedance/repos/toutiao/app_3/pytest_demo
plugins: schemathesis-1.1.0, cov-2.12.0, subtests-0.2.1, ordering-0.6, hypothesis-5.49.0
collected 2 items

test_timer.py::test_assert_one
Total start: 2021-06-01 11:29:32
PASSED
Time cost: 1.006s

test_timer.py::test_assert_two PASSED
Time cost: 2.006s
Total finished: 2021-06-01 11:29:35
Total cost: 3.015s


================================================================================================= 2 passed in 3.03s ==================================================================================================
```

### 测试覆盖率
使用 `pytest-cov` 进行代码测试覆盖率检查, 安装之后可以使用 `--cov` 参数来检查测试样例对指定代码目录的覆盖率，可以使用 `--cov-report` 输出测试报告。

```
pip install pytest-cov
pytest --cov=myproj tests/
```

## 参考文档
[pytest: helps you write better programs - pytest documentation](https://docs.pytest.org/en/latest/index.html)         
[Pytest 使用手册](https://learning-pytest.readthedocs.io/zh/latest/)           
[Welcome to pytest-cov’s documentation!](https://pytest-cov.readthedocs.io/en/latest/)         
[pytest-mock](https://github.com/pytest-dev/pytest-mock)              
[pytest文档4-测试用例setup和teardown](https://www.cnblogs.com/yoyoketang/p/9374957.html)      
[[接口测试_B] 06 Pytest的setup和teardown](https://www.jianshu.com/p/a57b5967f08b)          
[Python Mock的入门](https://segmentfault.com/a/1190000002965620)              
[Pytest权威教程(官方教程翻译)](https://www.cnblogs.com/superhin/p/11677240.html)            
[pytest测试框架中的setup和tearDown](https://python012.github.io/2018/05/08/pytest%E6%B5%8B%E8%AF%95%E6%A1%86%E6%9E%B6%E4%B8%AD%E7%9A%84setup%E5%92%8CtearDown/)               
[pytest中的fixture](https://note.qidong.name/2018/01/pytest-fixture/)        
[《pytest测试实战》-- Brian Okken](https://www.cnblogs.com/dongye95/p/13488235.html)          
