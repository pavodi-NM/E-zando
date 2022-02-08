    function executeQuery(){
        var query = document.getElementById("search_here").value;
        if (query){
        window.location.replace("{% url 'standardApps:search_produit' %}?search=" +query);
        return false;
            }
        }
        function executeQueryMobile(){
        var query = document.getElementById("search_here_mobile").value;
        if (query){
        window.location.replace("{% url 'standardApps:search_produit' %}?search=" +query);
        return false;
            }
    }