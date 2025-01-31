# 个人 使用 Playwright + Pytest + Allure 的测试框架试做
helpers 中集成日志打印，自动更新 Playwright 等功能
conftest 中主要集成 Playwright，pytest 配置和 allure 生成测试报告功能
testcase 中为测试用例，可以单挑执行后在 report 文件夹中查看 log 信息
# 运行方法
1. 安装依赖包
2. 执行 run_test.sh文件
3. 根目录`./report`文件夹下查看用例执行结果，allure 网站查看执行步骤