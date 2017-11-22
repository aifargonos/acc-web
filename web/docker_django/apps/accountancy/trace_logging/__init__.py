# TODO: [trace] module description
# FIXME: [trace] there should be a trace formatter; normal formatter fails if it has %(indent) and receives a message from normal logger. Also single_indent should be a parameter of this trace formatter.
# TODO: [trace] trace_level should be specified when the logger is used as a decorator and not in getLogger!
"""
A trace logger can be used as a decorator
that will log calling and exiting the function.
Each call increases indentation and each exit decreases it.
Logged messages are prefixed with the indentation.
"""

import io, os, sys, logging, traceback



if hasattr(sys, '_getframe'):
	currentframe = lambda: sys._getframe(3)
else: #pragma: no cover
	def currentframe():
		"""Return the frame object for the caller's stack frame."""
		try:
			raise Exception
		except Exception:
			return sys.exc_info()[2].tb_frame.f_back

_srcfile = os.path.normcase(currentframe.__code__.co_filename)



class BeforeAfter(object):
	"""
	A decorator that calls "before" before calling the underlying function,
	"after" after the call, and "on_exc" when the function is exiting because
	an unhandled exception was raised in it.
	
	Arguments passed to "before" are:
		"name" = name of the underlying function,
		"module" = module of the underlying function,
		"args" = *args passed to the underlying function
		"kwargs" = **kwargs passed to the underlying function
	
	Arguments passed to "after" are:
		"result" = result of calling the underlying function,
		"name" = name of the underlying function,
		"module" = module of the underlying function,
		"args" = *args passed to the underlying function
		"kwargs" = **kwargs passed to the underlying function
	
	Arguments passed to "on_exc" are:
		"exception" = the exception that was raised in the function,
		"name" = name of the underlying function,
		"module" = module of the underlying function,
		"args" = *args passed to the underlying function
		"kwargs" = **kwargs passed to the underlying function
	"""
	
	def __init__(self, before, after, on_exc):
		self._before = before
		self._after = after
		self._on_exc = on_exc
	
	def __call__(self, f):
		
		def result(*args, **kwargs):
			self._before(name=f.__name__, module=f.__module__, args=args, kwargs=kwargs)
			try:
				r = f(*args, **kwargs)
				self._after(result=r, name=f.__name__, module=f.__module__, args=args, kwargs=kwargs)
				return r
			except:
				self._on_exc(exception=sys.exc_info()[1], name=f.__name__, module=f.__module__, args=args, kwargs=kwargs)
				raise
		
		return result
	
	pass



class TraceFormatter(object):
	
	def __init__(self, defaultFormatter):
		self._default = defaultFormatter
	
	def format(self, record):
		if hasattr(record, "indent"):
			record.msg = record.indent + record.msg		
		return self._default.format(record)
	
	pass

logging._defaultFormatter = TraceFormatter(logging._defaultFormatter)



class TraceLogger(logging.Logger, BeforeAfter):
	
	def __init__(self, name, single_indent="  ", trace_level=logging.DEBUG, level=logging.NOTSET):
		logging.Logger.__init__(self, name, level)
		BeforeAfter.__init__(self,
			lambda *args, **kwargs: self._log_before(*args, **kwargs),
			lambda *args, **kwargs: self._log_after(*args, **kwargs),
			lambda *args, **kwargs: self._log_exc(*args, **kwargs),
		)
		self._trace_level = trace_level
		self._ind_count = 0
		self.single_indent = single_indent

	# This is coppied from logging, except the following line:
	# 	'filename in (logging._srcfile, _srcfile)'
	# It needs to extend the check to this source file.
	def findCaller(self, stack_info=False):
		"""
		Find the stack frame of the caller so that we can note the source
		file name, line number and function name.
		"""
		f = currentframe()
		#On some versions of IronPython, currentframe() returns None if
		#IronPython isn't run with -X:Frames.
		if f is not None:
			f = f.f_back
		rv = "(unknown file)", 0, "(unknown function)", None
		while hasattr(f, "f_code"):
			co = f.f_code
			filename = os.path.normcase(co.co_filename)
			if filename in (logging._srcfile, _srcfile):
				f = f.f_back
				continue
			sinfo = None
			if stack_info:
				sio = io.StringIO()
				sio.write('Stack (most recent call last):\n')
				traceback.print_stack(f, file=sio)
				sinfo = sio.getvalue()
				if sinfo[-1] == '\n':
					sinfo = sinfo[:-1]
				sio.close()
			rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
			break
		return rv

	def setTraceLevel(self, level):
		"""
		Set the logging level with which the tracing messages are logged.
		"""
		self._trace_level = logging._checkLevel(level)
	
	def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
		"""
		Adds indentation to the message and calls the superclass.
		"""
		if extra and "add_indent" in extra and extra["add_indent"] < 0:
			self._ind_count += extra["add_indent"]
		if extra is None:
			extra = dict()
		extra["indent"] = self.single_indent * self._ind_count
		if extra and "add_indent" in extra and extra["add_indent"] > 0:
			self._ind_count += extra["add_indent"]
		logging.Logger._log(self, level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info)
	
	def _log_before(self, name, module, args, kwargs):
		if not self.isEnabledFor(self._trace_level):
			return
		# else
		args_list = [repr(arg) for arg in args] + ['%s=%r' % item for item in kwargs.items()]
		self.log(self._trace_level, "call %s.%s(%s)" % (module, name, ", ".join(args_list)),
				extra={"add_indent": 1,
					"traced_name": name,
					"traced_module": module,
					"traced_args": args,
					"traced_kwargs": kwargs})
	
	def _log_after(self, result, name, module, args, kwargs):
		if not self.isEnabledFor(self._trace_level):
			return
		# else
		self.log(self._trace_level, "exit %s.%s = %r" % (module, name, result),
				extra={"add_indent": -1,
					"traced_result": result,
					"traced_name": name,
					"traced_module": module,
					"traced_args": args,
					"traced_kwargs": kwargs})
	
	def _log_exc(self, exception, name, module, args, kwargs):
		if not self.isEnabledFor(self._trace_level):
			return
		# else
		self.log(self._trace_level, "exception raised in %s.%s: %s" % (module, name, exception),
				extra={"add_indent": -1,
					"traced_exception": exception,
					"traced_name": name,
					"traced_module": module,
					"traced_args": args,
					"traced_kwargs": kwargs})
	
	pass



def getTraceLogger(name=None, trace_level=None, single_indent=None):
	logging._acquireLock()
	try:
		oldClass = logging.getLoggerClass()
		logging.setLoggerClass(TraceLogger)
		result = logging.getLogger(name)
		logging.setLoggerClass(oldClass)
		if single_indent is not None:
			result.single_indent = single_indent
		if trace_level is not None:
			result.setTraceLevel(trace_level)
		return result
	finally:
		logging._releaseLock()
	pass


