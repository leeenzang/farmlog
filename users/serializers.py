# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    
    # 비밀번호
    password = serializers.CharField(
        write_only=True,  # 출력할 땐 숨김
        required=True,    # 안 보내면 에러
        validators=[validate_password]  # 비밀번호 검증 로직
    )
    password2 = serializers.CharField(write_only=True, required=True)  # 비밀번호 확인용

    # 어떤 모델과 연결돼있는지, 어떤 필드를 처리할 건지 정의
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'nickname')

    # attrs는 프론트가 보낸 값들 모은 딕셔너리 중 비번 둘을 비교
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return attrs  #맞으면 통과 틀리면 ValidationError 발생

    def create(self, validated_data):
        validated_data.pop('password2')  # 이건 모델에 없으니까 버려
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
        )
        return user
    

# 로그인용 시얼라이저
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("아이디 또는 비밀번호가 잘못되었습니다.")
            attrs['user'] = user  # 나중에 view에서 쓰려고 저장해놓는거
        else:
            raise serializers.ValidationError("아이디와 비밀번호 모두 입력해야 합니다.")

        return attrs
    
    
# 회원 정보 수정
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'password')
        read_only_fields = ('username',)# 아이디는 수정 못 하게

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  # 비번은 set_password로 해싱해줘야 함
        return super().update(instance, validated_data)