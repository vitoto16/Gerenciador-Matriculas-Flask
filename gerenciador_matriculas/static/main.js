var listaAlunos = $("#lista-alunos");
var listaCursos = $("#lista-cursos");
var avisoAlunos = $("#aviso-alunos");
var avisoCursos = $("#aviso-cursos");
console.log(avisoCursos)
console.log(avisoAlunos)

var aluno = $(".article-aluno");
var curso = $(".article-curso");

$(function() {
    listaAlunos.click(function() {
        if (aluno.length) {
            aluno.fadeToggle(500);
        } else {
            avisoAlunos.fadeToggle(500);
        }
    });
    listaCursos.click(function() {
        if (curso.length) {
            curso.fadeToggle(500);
        } else {
            avisoCursos.fadeToggle(500);
        }
    });
});
