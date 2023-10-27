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
                         try {
                         if (Object.keys(data.options).length == 0){
                            options = '<option value="">Selecione curso</option>';
                         }
                         else{
                          for (var i = 0; i < Object.keys(data.options).length; i++) {
                            console.log(data.options[i].name)
                            options += '<option value="' + data.options[i].name +'">' + data.options[i].name + '</option>';

                        }
                        }
                        }
                        catch (e) {


                            options = '<option value="">Selecione curso</option>';


                        }

                        $('#secondOption').html(options);
                    }
                });
            });
        });