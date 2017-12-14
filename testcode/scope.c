#include<stdio.h>

int i=100;

void func()
{
    printf("%d\n",i);
}

int main()
{
    for(int i=0;i<1;i++)
    {
	printf("%d\n",i);
    }
//    i=99;
    int i=3;
    {
	int i=4;
    }
    printf("%d\n",i);

    func();
    return 0;
}


