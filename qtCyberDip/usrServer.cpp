#include "stdafx.h"
#include "usrServer.h"


#define	BUF_SIZE	1024
#define PORT_		19876


usrServer::usrServer(usrGameController* GC)
{
	controller = GC;
	qDebug() << "Server online.";
	
}

usrServer::~usrServer()
{
}


void usrServer::ServerRun()
{

	WSADATA wsd;
	int iRet = 0;

	// ��ʼ���׽��ֶ�̬��
	if (WSAStartup(MAKEWORD(2, 2), &wsd) != 0) {
		printf("WSAStartup failed:%d!\n", WSAGetLastError());
		
	}

	SOCKET socketSrv = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
	SOCKADDR_IN addrSrv;
	SOCKADDR_IN addrClient;
	char strRecv[BUF_SIZE] = { 0 }, strSend[BUF_SIZE] = "udp server send";
	int len = sizeof(SOCKADDR);

	// ���÷�������ַ
	ZeroMemory(strRecv, BUF_SIZE);
	addrSrv.sin_addr.s_addr = INADDR_ANY;
	//addrSrv.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(PORT_);

	// ���׽���
	iRet = bind(socketSrv, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR));
	if (SOCKET_ERROR == iRet)
	{
		printf("bind failed%d!\n", WSAGetLastError());
		closesocket(socketSrv);
		WSACleanup();
	}

	// �ӿͻ��˽�������
	printf("udp server start...\n");
	while (TRUE)
	{
		iRet = recvfrom(socketSrv, strRecv, BUF_SIZE, 0, (SOCKADDR*)&addrClient, &len);
		if (SOCKET_ERROR == iRet) {
			printf("recvfrom failed !\n");
			closesocket(socketSrv);
			WSACleanup();
			
		}

		printf("Recv From Client:%s\n", strRecv);

		// ��ͻ��˷�������
		sendto(socketSrv, strSend, sizeof(strSend), 0, (SOCKADDR*)&addrClient, len);
	}

	closesocket(socketSrv);
	WSACleanup();

}