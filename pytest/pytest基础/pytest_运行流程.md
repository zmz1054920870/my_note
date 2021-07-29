## [pytest运行流程](https://www.cnblogs.com/crystal1126/p/13293057.html)

pytest的整个测试简单分成如下6个阶段：

**1. pytest_configure**

　　插件和conftest.py文件配置初始化等，创建session。

**2、pytest_sessionstart**

　　创建session完以后，执行collection之前的阶段。会调用**pytest_report_header**向terminal打印一些环境信息，比如插件版本，python版本，操作平台这些等。

**3、pytest_collection**

　　测试用例收集以及生成测试输入的过程，这里还可能包括根据keywords和marker筛选测试用例的过程。这个过程会涉及多次generate item的调用，主要关注如下调用：

　　**pytest_generate_tests**(*metafunc*): 生成测试项；

　　**pytest_make_parametrize_id**(*config*, *val*, *argname*)：根据@pytest.mark.parametrize生成对应值；

　　**pytest_collection_modifyitems**(*session*, *config*, *items*)：所有测试项收集完毕以后调用，一般用来进行重新排序和二次过滤。

　　**pytest_deselected**(*items*): 有测试项被关键字或者marker过滤掉的时候会被调用

*注意： 通过`::`语法筛选测试用例的步骤是在之前生成测试用例阶段完成的，并不是在deselected里面做的*

**4、pytest_runtestloop**

　　执行筛选过的测试用例， 在**pytest_runtest_protocol**里面完成包括setup, call, teardown和log打印的过程。主要关注如下调用： 

　　**pytest_runtest_logstart**(*nodeid*, *location*)：开始执行一个新测试项的时候调用.

　　*注：官方文档的意思表述的有点模糊，并不是setup/call/teardown阶段分别调用一次，就是函数命令一直的意思测试开始前打印一次*

　　**pytest_runtest_logfinish**(*nodeid*, *location*): 结束执行一个测试项的时候调用.
　　*注：同上*

　　**pytest_runtest_setup**(*item*)： 在`pytest_runtest_call`执行之前调用.

　　**pytest_runtest_call**(*item*): 执行实际的测试过程。

　　**pytest_runtest_teardow**(*item*, *nextitem*): 在`pytest_runtest_call`执行之后调用

　　**pytest_fixture_setup**(*fixturedef*, *request*)：执行fixture的setup过程（是否执行取决于fixture是否需要创建）.

　　**pytest_fixture_post_finalizer**(*fixturedef*, *request*): 执行fixture的teardown过程（如果有）。

　　**pytest_runtest_makereport**(*item*, *call*): 返回给定item和call对应的 [`_pytest.runner.TestReport`](https://docs.pytest.org/en/latest/reference.html#_pytest.runner.TestReport) 对象, 这里的call object我们一般不太接触，_pytest/runner.py里面有具体的用法可以参考。

　　**pytest_runtest_logreport**(*report*): 在测试的setup/call/teardown阶段report更新之后分别被调用到，可以用when属性来区分不同阶段。

　　**pytest_report_teststatus**(*report*, *config*): 返回各个测试阶段的result, 可以用when属性来区分不同阶段。

**5、pytest_sessionfinish**

　　所有测试执行完毕之后，返回exit status之前的阶段。会调用**pytest_terminal_summary**向terminal打印一些summary信息，比如pass, fail, error数量之类的总结信息。

```
def pytest_terminal_summary(terminalreporter, exitstatus, config):

    '''收集测试结果'''

    print(terminalreporter.stats)

    print("total:", terminalreporter._numcollected)

    print('passed:', len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown']))

    print('failed:', len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown']))

    print('error:', len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown']))

    print('skipped:', len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown']))

    # terminalreporter._sessionstarttime 会话开始时间

    duration = time.time() - terminalreporter._sessionstarttime

    print('total times:', duration, 'seconds')
```

**6、pytest_unconfigure**

　　session结束以后，整个process退出之前的阶段。

