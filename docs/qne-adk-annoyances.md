# 60 second delay and hidden error when application throws any exception

If the QNE-ADK application throws an exception (any exception, it doesn't matter which one) then
the application hangs for 60 seconds.

After 60 seconds we get a very generic `TimeoutExpired` exception error message.

The original exception that the application threw is hidden deep inside a block of text that
is barely readable because all the newlines have been replaced by backslash-n:

```
Results:
{
  "error": {
    "exception": "TimeoutExpired",
    "message": "Call to simulator timed out after 60 seconds.",
    "trace": "Traceback (most recent call last):\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/bin/netqasm\", line 8, in <module>\n    sys.exit(cli())\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/click/core.py\", line 1130, in __call__\n    return self.main(*args, **kwargs)\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/click/core.py\", line 1055, in main\n    rv = self.invoke(ctx)\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/click/core.py\", line 1657, in invoke\n    return _process_result(sub_ctx.command.invoke(sub_ctx))\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/click/core.py\", line 1404, in invoke\n    return ctx.invoke(self.callback, **ctx.params)\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/click/core.py\", line 760, in invoke\n    return __callback(*args, **kwargs)\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/netqasm/runtime/cli.py\", line 344, in simulate\n    simulate_application(\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/squidasm/run/multithread/simulate.py\", line 89, in simulate_application\n    result = mgr.run_app(app_instance, use_app_config=use_app_config)\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/venv/lib/python3.8/site-packages/squidasm/run/multithread/runtime_mgr.py\", line 204, in run_app\n    results[name] = future.get()\n  File \"/usr/local/Cellar/python@3.8/3.8.14/Frameworks/Python.framework/Versions/3.8/lib/python3.8/multiprocessing/pool.py\", line 771, in get\n    raise self._value\n  File \"/usr/local/Cellar/python@3.8/3.8.14/Frameworks/Python.framework/Versions/3.8/lib/python3.8/multiprocessing/pool.py\", line 125, in worker\n    result = (True, func(*args, **kwds))\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/qne_adk/dqft/dqft_experiment/input/app_bob.py\", line 68, in main\n    processor = Processor(nr_processors=2, total_nr_qubits=4, processor_index=1, logger=app_logger)\n  File \"/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022/qne_adk/dqft/dqft_experiment/input/app_bob.py\", line 17, in __init__\n    self.logger(f\"Create processor {name}\")\nNameError: name 'name' is not defined\n"
  }
}
```




