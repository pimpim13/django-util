$(function () {

  // Ajout style bootstrap sur tous les élements de formulaire
  $("input:not([type='checkbox']),select,textarea").addClass("form-control");
  $("input[type='checkbox']").addClass("form-control-input");
  $("input[type='hidden']").parent(".form-group").hide()
  // Déclenchement des tooltips
  $('[data-toggle="tooltip"]').tooltip();

  $(document).on('select2:open', () => {
    document.querySelector('.select2-search__field').focus();
  });
})
