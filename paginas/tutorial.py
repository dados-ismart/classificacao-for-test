import streamlit as st

st.title('Tutorial de uso')

st.link_button('Tutorial', r'https://ismartorg-my.sharepoint.com/my?id=%2Fpersonal%2Ffelipe%5Famaral%5Fismart%5Forg%5Fbr%2FDocuments%2Ftutorial%5Fclassificacao&ga=1')
st.video(r'https://ismartorg-my.sharepoint.com/personal/felipe_amaral_ismart_org_br/_layouts/15/stream.aspx?id=%2Fpersonal%2Ffelipe%5Famaral%5Fismart%5Forg%5Fbr%2FDocuments%2Ftutorial%5Fclassificacao%2Ftutorial%5Fclassificacao%5Fcoordenadoras%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2Ea56c548b%2D5133%2D4e3a%2Db1bd%2D17699da8aa02')
st.header('Categorias de avaliação (baseadas apenas nas notas):')
st.markdown('''
❌ **Crítico Escolar** - 1 nota com diferença menor que 1 ponto da média ou mais de 2 notas abaixo da média  
⚠️ **Atenção Escolar** - até 2 notas abaixo da média  
➖ **Mediano Escolar** - nenhuma nota abaixo da média  
🔶 **Pré-Destaque Escolar** - mais de 2 notas com diferença maior que 2 pontos da média e pelo menos 1 com diferença maior que 1 ponto da média  
⭐ **Destaque Escolar** - 5 notas com diferença maior que 2 pontos da média
''')