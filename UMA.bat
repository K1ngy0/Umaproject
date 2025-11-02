@echo off
setlocal enabledelayedexpansion

REM 定义检查的JSON文件和要执行的批处理文件
set "json_file=windows_videos.json"
set "server_bat=start_server.bat"
set "py_script=Umaproject.py"


REM 检查JSON文件是否存在
if exist "%json_file%" (
    echo 发现%json_file%，准备启动服务器...
    echo.

    REM 检查start_server.bat是否存在
    if not exist "%server_bat%" (
        echo 错误：未找到%server_bat%文件，请确认文件存在
        pause
        exit /b 1
    )

    REM 执行启动服务器脚本
    echo 正在运行%server_bat%...
    echo ==============================================
    call "%server_bat%"



    REM 显示服务器脚本执行结果
    if %errorlevel% equ 0 (
        echo ==============================================
        echo %server_bat%执行完成
    ) else (
        echo ==============================================
        echo %server_bat%执行失败，错误代码：%errorlevel%
    )
) else (
    echo 未找到%json_file%，准备执行视频扫描...
    echo.

    REM 检查Python环境
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo 错误：未找到Python环境，请确保Python已安装并添加到环境变量
        pause
        exit /b 1
    )

    REM 检查Python脚本是否存在
    if not exist "%py_script%" (
        echo 错误：未找到%py_script%文件，请确认文件存在
        pause
        exit /b 1
    )

    REM 显示参数说明
    echo ==============================================
    echo 视频扫描脚本参数输入
    echo 支持的参数格式示例：
    echo   -r "扫描目录路径" -s "服务器根目录"  -min 最小大小(MB)
    echo 例如：
    echo   -r "D:\Videos" -s "D:\VideoServer"  -min 5
    echo ==============================================

    REM 读取用户输入的参数
    set /p "params=请输入参数: "

    REM 运行Python脚本并传递参数
    echo.
    echo 正在执行%py_script%...
    echo ==============================================
    python "%py_script%" %params%

    REM 显示Python脚本执行结果
    if %errorlevel% equ 0 (
        echo ==============================================
        echo %py_script%执行完成
        call "%server_bat%"
	
    ) else (
        echo ==============================================
        echo %py_script%执行失败，错误代码：%errorlevel%
    )
)

REM 暂停以查看输出
pause
endlocal