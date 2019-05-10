#ifdef VIA_OPENCV

#ifndef USRGAMECONTROLLER_H
#define USRGAMECONTROLLER_H

#include "qtcyberdip.h"
#include <stdio.h> 
#include <stdlib.h> 
//#include <winsock2.h>
#include <string.h> 



#define WIN_NAME "Frame"


//��Ϸ������
class usrGameController
{
private:
	deviceCyberDip* device;
//������Ϊ��ʵ����ʾЧ�������ӵ�����
	//���ص��ṹ��
	struct MouseArgs{
		cv::Rect box;
		bool Drawing, Hit;
		// init
		MouseArgs() :Drawing(false), Hit(false)
		{
			box = cv::Rect(0, 0, -1, -1);
		}
	};
	//���ص�����
	friend void  mouseCallback(int event, int x, int y, int flags, void*param);
	MouseArgs argM;
//������Ϊ��ʵ�ֿ�����ʾЧ�������ӵ�����
//������Ϊ��ʵ�ֿκ���ҵʵ�֣����ӵ�����
	
public:
	//���캯�������б����ĳ�ʼ����Ӧ�ڴ����
	usrGameController(void* qtCD);
	//�������������ձ���������Դ
	~usrGameController();
	//����ͼ������ÿ���յ�ͼ��ʱ�������
	int usrProcessImage(cv::Mat& img);
	//��ʾͼ������ÿ���յ�ͼ��ʱ������ã�������QTUI����������ı��
	cv::Mat usrDisplayImage(cv::Mat& img);

};

//������Ϊ��ʵ����ʾЧ�������ӵ�����
//���ص�����
void  mouseCallback(int event, int x, int y, int flags, void*param);
//������Ϊ��ʵ�ֿ�����ʾЧ�������ӵ�����

//class usrServer
//{
//private:
//	usrGameController* controller;
//public:
//	int serving();
//};


#endif
#endif