from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField


from core.models import Compra, ItensCompra

class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade
    
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 1

class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")

class CompraSerializer(ModelSerializer):
    status = CharField(source="get_status_display", read_only=True)
    usuario = CharField(source="usuario.email", read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)
    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "itens")


class CompraCreateUpdateSerializer(ModelSerializer):
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ("usuario", "itens")

    def create(self, validated_data):
        itens_data = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item_data in itens_data:
            ItensCompra.objects.create(compra=compra, **item_data)
        compra.save()
        return compra

    def update(self, compra, validated_data):
        itens_data = validated_data.pop("itens")
        if itens_data:
            compra.itens.all().delete()
            for item_data in itens_data:
                ItensCompra.objects.create(compra=compra, **item_data)
        return super().update(compra, validated_data)
    
class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source="livro.titulo", read_only=True)

    class Meta:
        model = ItensCompra
        fields = ("quantidade", "livro")
        depth = 1    

class CompraListSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ("id", "usuario", "itens")    

