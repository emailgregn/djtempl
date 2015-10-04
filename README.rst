About
-----
Render a dockerfile from a template and pip requirements.txt.
Docker caches each dockerfile command in it's own layer.
By breaking out requirements.txt, each pip requirement goes into its own layer and build time improves.

Handles all the syntax allowed by `pip <https://pip.pypa.io/en/stable/>`_ in `requirements.txt <https://pip.pypa.io/en/stable/user_guide/#requirements-files>`_



Things like comments, whitespace, line continuations etc. that might choke a simpler solution. Uses the actual parser from pip so guaranteed\* compatibility

\* or your money back

Usage
-----

Start with a copy your regular Dockerfile called Dockerfile.tmpl

Replace the pip install command that looks something like this::

    RUN pip install -r requirements.txt


with some standard django template tags like this::

    {% for req in pip_requirements %}
    RUN pip install --upgrade {{ req }}{% endfor%}


djtempl will pass in a tuple called ``pip_requirements`` into the template context.

.. code:: bash

    python djtempl.py -t ./Dockerfile.tmpl -p ./requirements.txt -d ./Dockerfile.out -q



Installation
------------

.. code:: bash

    pip install djtempl


`djtempl.py <https://raw.githubusercontent.com/emailgregn/djtempl/master/djtempl/djtempl.py>`_
is pure python and only requires django>=1.8.0


Contributing
------------
Bug Reports & Feature Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please use the `issue tracker <https://github.com/emailgregn/djtempl/issues>`__
to report any bugs or file feature requests.