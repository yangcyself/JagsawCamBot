#ifdef VIA_OPENCV

#ifndef USRGAMECONTROLLER_H
#define USRGAMECONTROLLER_H

#include "qtcyberdip.h"
#include <stdio.h> 
#include <stdlib.h> 
//#include <winsock2.h>
#include <string.h> 



#define WIN_NAME "Frame"


//游戏控制类
class usrGameController
{
private:
	cv::Mat currentFrame;
	deviceCyberDip* device;
//以下是为了实现演示效果，增加的内容
	//鼠标回调结构体
	struct MouseArgs{
		cv::Rect box;
		bool Drawing, Hit;
		// init
		MouseArgs() :Drawing(false), Hit(false)
		{
			box = cv::Rect(0, 0, -1, -1);
		}
	};
	//鼠标回调函数
	friend void  mouseCallback(int event, int x, int y, int flags, void*param);
	MouseArgs argM;
//以上是为了实现课堂演示效果，增加的内容
//以下是为了实现课后作业实现，增加的内容
	
public:
	//构造函数，所有变量的初始化都应在此完成
	usrGameController(void* qtCD);
	//析构函数，回收本类所有资源
	~usrGameController();
	//处理图像函数，每次收到图像时都会调用
	int usrProcessImage(cv::Mat& img);
	//显示图像函数，每次收到图像时都会调用，用于在QTUI中做有意义的标记
	cv::Mat usrDisplayImage(cv::Mat& img);
	cv::Mat currentImage();

};

//以下是为了实现演示效果，增加的内容
//鼠标回调函数
void  mouseCallback(int event, int x, int y, int flags, void*param);
//以上是为了实现课堂演示效果，增加的内容

//class usrServer
//{
//private:
//	usrGameController* controller;
//public:
//	int serving();
//};


#endif
#endif