<a href="#" onclick="document.getElementById('logout-form').submit();">Logout</a>
<form id="logout-form" action="{% url 'logout' %}" method="post" style="display: none;">
    {% csrf_token %}
</form>
