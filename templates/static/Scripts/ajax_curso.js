 $(document).ready(function() {
            $('#firstOption').change(function() {
                var firstOptionId = $(this).val();
                $.ajax({

                    url: '/cursos/',
                    data: {
                        'curs_codigo': firstOptionId
                    },
                    success: function(data) {

                        var options = '';
                        for (var i = 0; i < Object.keys(data).length; i++) {
                            console.log(data.options[i].name)
                            options += '<option value="' + data.options[i].name + '">' + data.options[i].name + '</option>';

                        }
                        $('#secondOption').html(options);
                    }
                });
            });
        });