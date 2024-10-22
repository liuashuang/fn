import boto3
from botocore.exceptions import ClientError

# 配置 AWS 凭证
aws_access_key = 'AKIAYSE4OACROAQYVMB2'  # 替换为您的访问密钥 ID
aws_secret_key = 'BAzsClxZyqQXMARfTmjWZtxqVZKMp0wct6pLKUYhmgVy'   # 替换为您的秘密密钥
region = 'ap-southeast-2'  # 更改为您的区域

# 创建 SES 客户端
ses_client = boto3.client(
    'ses',
    region_name=region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# 发送邮件
try:
    response = ses_client.send_email(
        Source='liuashuang889@gmail.com',  # 替换为验证的发件人邮箱
        Destination={
            'ToAddresses': [
                '1006174519@qq.com',  # 替换为收件人邮箱
            ],
        },
        Message={
            'Subject': {
                'Data': '测试邮件',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': '这是一封通过 Amazon SES 发送的测试邮件。',
                    'Charset': 'UTF-8'
                },
            }
        }
    )
except ClientError as e:
    print(f"发送失败: {e.response['Error']['Message']}")
else:
    print("邮件发送成功，Message ID:", response['MessageId'])
