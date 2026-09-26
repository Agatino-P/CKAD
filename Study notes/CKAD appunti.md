<style>
mark{
  background-color: lightgrey;
  color: black;
  font-weight: bold;
}
body {
  counter-reset: h1;
}

h1 {
  font-size: 1.5em;
  font-weight: bold;
  counter-reset: h2;
}

h2 {
  font-size: 1.4em;
  font-weight: bold;
  counter-reset: h3;
}

h3 {
  font-size: 1.3em;
  font-style: italic;
  counter-reset: h4;
  margin-left: 1em;
}

h4 {
  font-size: 1.2em;
  font-style: italic;
  counter-reset: h5;
  margin-left: 1em;
}

h5 {
  font-size: 1.1em;
  font-style: italic;
  counter-reset: h6;
  margin-left: 1em;
}

h6 {
  font-size: 1em;
  font-style: italic;
  margin-left: 1em;
}

h1:before {
  counter-increment: h1;
  content: counter(h1) ". "
}

h2:before {
  counter-increment: h2;
  content: " " counter(h1) "." counter(h2) ". "
}

h3:before {
  counter-increment: h3;
  content: counter(h1) "." counter(h2) "." counter(h3) ". "
}

h4:before {
  counter-increment: h4;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) ". "
}

h5:before {
  counter-increment: h5;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) ". "
}

h6:before {
  counter-increment: h6;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) "." counter(h6) ". "
}

</style>

> **AUDIT BASELINE — 2026-09-26**
> CKAD currently uses Kubernetes v1.35; recheck near exam day because the exam environment is aligned with the newest Kubernetes minor release within approximately 4 to 8 weeks of that release.
> Ref: [CKAD FAQ](https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks) · [v1.35 docs](https://v1-35.docs.kubernetes.io/docs/)
